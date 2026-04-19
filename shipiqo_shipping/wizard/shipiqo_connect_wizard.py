import requests
from odoo import models, fields, _
from odoo.exceptions import UserError

class ShipiqoConnectWizard(models.TransientModel):
    _name = 'shipiqo.connect.wizard'
    _description = 'Connect to Shipiqo'

    shop_url = fields.Char(string='Your Odoo URL', required=True, default=lambda self: self.env['ir.config_parameter'].sudo().get_param('web.base.url'))
    auth_url = fields.Char(string='Shipiqo Authorization URL', readonly=True,
                           default='https://shipiqo.com/odoo/auth')
    api_key = fields.Char(string='Paste API Key from Shipiqo', help='After authorizing, paste the API key shown in Shipiqo here')
    webhook_secret = fields.Char(string='Webhook Secret')

    def action_save(self):
        if not self.api_key:
            raise UserError(_('Please paste the API Key from Shipiqo.'))
        settings = self.env['shipiqo.settings'].search([], limit=1)
        vals = {'shop_url': self.shop_url, 'api_key': self.api_key, 'webhook_secret': self.webhook_secret, 'is_active': True}
        if settings:
            settings.write(vals)
        else:
            settings = self.env['shipiqo.settings'].create(vals)
        # Ping
        try:
            r = requests.post(settings.api_endpoint, json={'action': 'ping'}, headers={'x-shipiqo-key': settings.api_key}, timeout=10)
            data = r.json()
            if not data.get('success'):
                raise UserError(_('Connection test failed: %s') % data.get('error', 'unknown'))
        except Exception as e:
            raise UserError(_('Connection error: %s') % e)
        return {
            'type': 'ir.actions.client', 'tag': 'display_notification',
            'params': {'title': _('Connected!'), 'message': _('Shipiqo is now active. Open any sales order to see the widget.'), 'type': 'success', 'sticky': False},
        }
