{
    'name': 'Shipiqo Shipping',
    'version': '2.0.0',
    'category': 'Inventory/Delivery',
    'summary': 'Multi-carrier shipping with embedded lifecycle widget on sales orders',
    'description': """
Shipiqo Shipping for Odoo
=========================
Connect your Odoo to Shipiqo and get:

* Real-time shipping rates from 50+ carriers directly on the sales order
* One-click rate selection that adds the carrier to the order
* Embedded lifecycle widget on every sales order with:
  - Rate comparison and selection (cheapest/fastest highlighted)
  - Tracking timeline once the order is confirmed
  - Direct chat with the carrier handling the shipment
  - Proof of delivery and shipping documents
* Zero technical configuration — install, click "Connect", done.

Compatible with Odoo 17 and Odoo 18.
    """,
    'author': 'Shipiqo ApS',
    'website': 'https://shipiqo.com',
    'license': 'OPL-1',
    'depends': ['delivery', 'sale_management', 'stock', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'data/delivery_carrier_data.xml',
        'views/shipiqo_settings_views.xml',
        'views/sale_order_views.xml',
        'views/delivery_carrier_views.xml',
        'wizard/shipiqo_connect_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'shipiqo_shipping/static/src/js/shipiqo_lifecycle_widget.js',
            'shipiqo_shipping/static/src/xml/shipiqo_lifecycle_widget.xml',
            'shipiqo_shipping/static/src/scss/shipiqo_widget.scss',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
