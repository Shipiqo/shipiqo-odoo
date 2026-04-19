from odoo import models, fields, api

class ShipiqoSettings(models.Model):
    _name = 'shipiqo.settings'
    _description = 'Shipiqo Connection Settings'
    _rec_name = 'shop_url'

    shop_url = fields.Char(string='Odoo Instance URL', required=True)
    api_key = fields.Char(string='Shipiqo API Key', required=True)
    webhook_secret = fields.Char(string='Webhook Secret')
    api_endpoint = fields.Char(
        string='Shipiqo API Endpoint',
        default='https://acgntxhujbknhckarssh.supabase.co/functions/v1/odoo-api',
        required=True,
    )
    embed_base_url = fields.Char(
        string='Widget Embed Base URL',
        default='https://shipiqo.com/embed/lifecycle',
        required=True,
    )
    is_active = fields.Boolean(default=True)
    last_sync_at = fields.Datetime(string='Last Sync')

    @api.model
    def get_active_settings(self):
        return self.search([('is_active', '=', True)], limit=1)
