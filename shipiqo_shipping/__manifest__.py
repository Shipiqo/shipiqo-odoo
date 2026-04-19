# -*- coding: utf-8 -*-
{
    "name": "Shipiqo Shipping",
    "version": "17.0.2.0.0",
    "summary": "Real-time freight rates, shipment tracking & lifecycle widget for 100+ carriers",
    "description": """
Shipiqo Shipping Integration
============================

Connect Odoo to **Shipiqo** — the modern multi-carrier shipping platform — and
get real-time freight rates from 100+ carriers directly in your sales orders,
quotations and delivery flows.

Features
--------
* 🚚 **Real-time rates** at quote and checkout time (parcel, pallet, FTL, sea, air)
* 📦 **Automatic shipment creation** when sales orders are confirmed
* 📍 **Lifecycle widget** on sales orders showing live tracking, ETA and exceptions
* 💬 **Two-way messaging** with carriers directly from Odoo
* 🏷️ **Label printing** (PDF & ZPL) without leaving Odoo
* 🌍 **International support** (EU, UK, US, Asia) with customs handling
* 🔐 **Secure** OAuth-style onboarding — no manual API key management

Subscription required
---------------------
⚠️ This module requires an active **Shipiqo Pro** or **Enterprise** subscription.

* Free / Basic plans: ❌ Not supported
* Pro plan (€199/mo): ✅ Full Odoo integration
* Enterprise plan: ✅ Full Odoo integration + white-label

Sign up at https://shipiqo.com — 14-day free trial available, no credit card required.

Without a Pro/Enterprise subscription the connection wizard will guide you to upgrade.
The module installs cleanly in any case but rate lookups will be blocked until upgrade.

Setup
-----
1. Install module
2. Settings → Shipiqo → Connect (4-step wizard)
3. Authorize with your Shipiqo account
4. Done — rates appear in sales orders immediately

Support
-------
* Documentation: https://shipiqo.com/docs/odoo
* Email: support@shipiqo.com
* Issues: https://github.com/Shipiqo/shipiqo-odoo/issues
""",
    "author": "Shipiqo ApS",
    "website": "https://shipiqo.com",
    "support": "support@shipiqo.com",
    "license": "OPL-1",
    "category": "Inventory/Delivery",
    "price": 0.0,
    "currency": "EUR",
    "depends": [
        "base",
        "sale_management",
        "delivery",
        "stock",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/delivery_carrier_data.xml",
        "views/delivery_carrier_views.xml",
        "views/sale_order_views.xml",
        "views/shipiqo_settings_views.xml",
        "wizard/shipiqo_connect_wizard_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "shipiqo_shipping/static/src/js/shipiqo_lifecycle_widget.js",
            "shipiqo_shipping/static/src/scss/shipiqo_widget.scss",
            "shipiqo_shipping/static/src/xml/shipiqo_lifecycle_widget.xml",
        ],
    },
    "images": ["static/description/icon.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
