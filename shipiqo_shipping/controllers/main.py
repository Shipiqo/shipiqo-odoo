from odoo import http
from odoo.http import request

class ShipiqoController(http.Controller):

    @http.route('/shipiqo/order/<int:order_id>/select_rate', type='json', auth='user')
    def select_rate(self, order_id, rate_id=None, carrier=None, product=None, price=None, currency='DKK', **kw):
        order = request.env['sale.order'].browse(order_id)
        if not order.exists():
            return {'error': 'Order not found'}
        # Find or create a delivery.carrier mapping for this Shipiqo product
        carrier_rec = request.env['delivery.carrier'].sudo().search([
            ('delivery_type', '=', 'shipiqo'),
            ('shipiqo_product_code', '=', rate_id or product),
        ], limit=1)
        if not carrier_rec:
            carrier_rec = request.env['delivery.carrier'].sudo().create({
                'name': f'Shipiqo · {carrier} {product}',
                'delivery_type': 'shipiqo',
                'shipiqo_product_code': rate_id or product,
                'product_id': request.env.ref('delivery.product_product_delivery').id,
                'fixed_price': float(price or 0),
            })
        order.set_delivery_line(carrier_rec, float(price or 0))
        order.shipiqo_pending_rate = f'{carrier} · {product}'
        return {'ok': True}

    @http.route('/shipiqo/order/<int:order_id>/skip_rate', type='json', auth='user')
    def skip_rate(self, order_id, **kw):
        order = request.env['sale.order'].browse(order_id)
        if order.exists():
            order.shipiqo_pending_rate = 'Customer arranges shipping'
        return {'ok': True}
