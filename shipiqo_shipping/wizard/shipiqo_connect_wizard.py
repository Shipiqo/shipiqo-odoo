# -*- coding: utf-8 -*-
import json
import logging
import requests
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

SHIPIQO_API_URL = "https://acgntxhujbknhckarssh.supabase.co/functions/v1/odoo-api"
SHIPIQO_AUTH_URL = "https://acgntxhujbknhckarssh.supabase.co/functions/v1/odoo-auth/exchange"


class ShipiqoConnectWizard(models.TransientModel):
    _name = "shipiqo.connect.wizard"
    _description = "Shipiqo Connection Wizard"

    state = fields.Selection(
        [
            ("step1", "Welcome"),
            ("step2", "Authorize"),
            ("step3", "Test Connection"),
            ("step4", "Done"),
        ],
        default="step1",
    )

    auth_code = fields.Char(string="Authorization Code")
    api_key = fields.Char(string="API Key", readonly=True)
    webhook_secret = fields.Char(string="Webhook Secret", readonly=True)
    api_url = fields.Char(string="API URL", readonly=True, default=SHIPIQO_API_URL)
    test_result = fields.Text(string="Test Result", readonly=True)
    error_message = fields.Html(string="Error", readonly=True)

    # ── Step navigation ──

    def action_next(self):
        self.ensure_one()
        if self.state == "step1":
            self.state = "step2"
        elif self.state == "step2":
            self._exchange_auth_code()
        elif self.state == "step3":
            self._test_connection()
        elif self.state == "step4":
            return {"type": "ir.actions.act_window_close"}
        return self._reopen()

    def action_back(self):
        self.ensure_one()
        order = ["step1", "step2", "step3", "step4"]
        idx = order.index(self.state)
        if idx > 0:
            self.state = order[idx - 1]
        return self._reopen()

    def _reopen(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    # ── Step 2: exchange auth code → API key ──

    def _exchange_auth_code(self):
        if not self.auth_code:
            raise UserError(_("Please paste the authorization code from Shipiqo."))

        try:
            response = requests.post(
                SHIPIQO_AUTH_URL,
                json={"code": self.auth_code.strip()},
                timeout=15,
            )
        except requests.RequestException as e:
            raise UserError(_("Could not reach Shipiqo: %s") % e)

        if response.status_code != 200:
            raise UserError(
                _("Failed to exchange code (HTTP %s): %s")
                % (response.status_code, response.text[:300])
            )

        data = response.json()
        self.write({
            "api_key": data.get("api_key"),
            "webhook_secret": data.get("webhook_secret"),
            "api_url": data.get("api_url", SHIPIQO_API_URL),
            "state": "step3",
        })

    # ── Step 3: test connection (handles tier gating) ──

    def _test_connection(self):
        if not self.api_key:
            raise UserError(_("Missing API key. Please go back and authorize again."))

        headers = {
            "Content-Type": "application/json",
            "x-shipiqo-key": self.api_key,
        }

        # 1) Ping — verifies key is valid (tier check is skipped for ping)
        try:
            ping = requests.post(
                self.api_url,
                json={"action": "ping"},
                headers=headers,
                timeout=15,
            )
        except requests.RequestException as e:
            raise UserError(_("Could not reach Shipiqo API: %s") % e)

        if ping.status_code != 200:
            raise UserError(
                _("Connection test failed (HTTP %s): %s")
                % (ping.status_code, ping.text[:300])
            )

        # 2) Live test — triggers tier check
        try:
            test = requests.post(
                self.api_url,
                json={
                    "action": "get_rates",
                    "params": {
                        "from_country": "DK",
                        "from_postal_code": "1000",
                        "to_country": "DK",
                        "to_postal_code": "2100",
                        "weight_kg": 1,
                        "segment": "PARCEL",
                    },
                },
                headers=headers,
                timeout=20,
            )
        except requests.RequestException as e:
            raise UserError(_("Could not reach Shipiqo API: %s") % e)

        # ── TIER GATING: handle 402 Payment Required ──
        if test.status_code == 402:
            try:
                payload = test.json()
            except ValueError:
                payload = {}

            if payload.get("code") == "TIER_REQUIRED":
                upgrade_url = payload.get(
                    "upgrade_url", "https://shipiqo.com/app/subscription"
                )
                self.error_message = _(
                    "<h3 style='color:#dc2626;'>⚠️ Subscription upgrade required</h3>"
                    "<p>Your Shipiqo plan does not include the Odoo integration.</p>"
                    "<p><b>Odoo requires the Shipiqo Pro or Enterprise plan.</b></p>"
                    "<p>Upgrade your plan to continue:<br/>"
                    "<a href='%s' target='_blank' "
                    "style='display:inline-block;margin-top:8px;padding:8px 16px;"
                    "background:#2563eb;color:white;border-radius:6px;"
                    "text-decoration:none;'>Upgrade to Pro →</a></p>"
                    "<p style='color:#6b7280;font-size:12px;margin-top:16px;'>"
                    "Already upgraded? Wait 1 minute and click 'Test connection' again."
                    "</p>"
                ) % upgrade_url
                # Stay on step3 so user can retry after upgrading
                return

            raise UserError(_("Subscription error: %s") % payload.get("error", test.text[:300]))

        if test.status_code != 200:
            raise UserError(
                _("Test rate request failed (HTTP %s): %s")
                % (test.status_code, test.text[:300])
            )

        result = test.json()
        rate_count = len(result.get("rates", []))

        # Save credentials to settings
        settings = self.env["shipiqo.settings"].sudo().search([], limit=1)
        if not settings:
            settings = self.env["shipiqo.settings"].sudo().create({})
        settings.write({
            "api_key": self.api_key,
            "webhook_secret": self.webhook_secret,
            "api_url": self.api_url,
            "is_connected": True,
        })

        self.test_result = _(
            "✅ Connection successful!\n\n"
            "Found %s test rate(s) for DK → DK route.\n"
            "Your Shipiqo integration is now active."
        ) % rate_count
        self.state = "step4"
