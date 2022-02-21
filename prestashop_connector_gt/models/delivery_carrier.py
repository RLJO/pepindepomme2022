# Copyright 2021 CTO IT Consulting
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    presta_id = fields.Char(string="Presta ID")
    delay_comment = fields.Char(string="Delay")
    is_presta = fields.Boolean(string="Presta")
    shop_ids = fields.Many2many('sale.shop', 'carrier_shop_rel', 'product_id', 'shop_id', string="Shop")

    
    def set_delivery(self, order, carrier_id):
        wizard = self.env['choose.delivery.carrier'].create({
            'order_id': order.id,
            'carrier_id': carrier_id,
        })
        wizard._get_shipment_rate()
        wizard.button_confirm()
