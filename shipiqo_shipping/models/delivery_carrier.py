import requests
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[('shipiqo', 'Shipiqo')], ondelete={'shipiqo': 'set default'})
    shipiqo_product_code = fields.Char(string='Shipiqo Product Code')

    def shipiqo_rate_shipment(self, order):
        settings = self.env['shipiqo.settings'].get_active_settings()
        if not settings:
            return {'success': False, 'price': 0.0, 'error_message': _('Shipiqo not configured'), 'warning_message': False}

        payload = {
            'action': 'get_rates',
            'params': {
                'from_country': order.warehouse_id.partner_id.country_id.code or 'DK',
                'from_postal_code': order.warehouse_id.partner_id.zip or '',
                'to_country': order.partner_shipping_id.country_id.code or 'DK',
                'to_postal_code': order.partner_shipping_id.zip or '',
                'segment': 'PARCEL',
                'parcels': [{
                    'weight_kg': sum(line.product_id.weight * line.product_uom_qty for line in order.order_line) or 1,
                    'length_cm': 30, 'width_cm': 20, 'height_cm': 15,
                }],
            },
        }
        try:
            r = requests.post(settings.api_endpoint, json=payload, headers={'x-shipiqo-key': settings.api_key}, timeout=15)
            data = r.json()
            if not data.get('success') or not data.get('rates'):
                return {'success': False, 'price': 0.0, 'error_message': data.get('error', 'No rates'), 'warning_message': False}
            cheapest = min(data['rates'], key=lambda x: x['price'])
            return {'success': True, 'price': cheapest['price'], 'error_message': False, 'warning_message': False}
        except Exception as e:
            _logger.exception('Shipiqo rate error')
            return {'success': False, 'price': 0.0, 'error_message': str(e), 'warning_message': False}
