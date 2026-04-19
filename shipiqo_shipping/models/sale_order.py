from urllib.parse import urlencode
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipiqo_shipment_id = fields.Char(string='Shipiqo Shipment ID', copy=False)
    shipiqo_widget_url = fields.Char(string='Shipiqo Widget URL', compute='_compute_shipiqo_widget_url')
    shipiqo_pending_rate = fields.Char(string='Pending Carrier', copy=False, help='Carrier selected in widget but not yet booked')

    @api.depends('id', 'shipiqo_shipment_id', 'state')
    def _compute_shipiqo_widget_url(self):
        settings = self.env['shipiqo.settings'].get_active_settings()
        for order in self:
            if not settings or not order.id:
                order.shipiqo_widget_url = False
                continue
            params = {
                'session': settings.api_key,
                'order_id': str(order.id),
                'system': 'odoo',
                'currency': order.currency_id.name or 'DKK',
                'locale': self.env.user.lang or 'en',
            }
            if order.shipiqo_shipment_id:
                params['shipment_id'] = order.shipiqo_shipment_id
            order.shipiqo_widget_url = f"{settings.embed_base_url}?{urlencode(params)}"

    def action_shipiqo_book_pending(self):
        """Called when sales order is confirmed (quotation -> sale)
        Promotes a pending shipment to a real one via the API."""
        settings = self.env['shipiqo.settings'].get_active_settings()
        if not settings:
            return
        for order in self.filtered(lambda o: o.shipiqo_shipment_id):
            try:
                import requests
                requests.post(settings.api_endpoint,
                    json={'action': 'confirm_shipment', 'params': {'shipment_id': order.shipiqo_shipment_id}},
                    headers={'x-shipiqo-key': settings.api_key}, timeout=10)
            except Exception:
                pass

    def action_confirm(self):
        res = super().action_confirm()
        self.action_shipiqo_book_pending()
        return res
