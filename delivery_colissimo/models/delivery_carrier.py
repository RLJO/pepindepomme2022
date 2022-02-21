# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class DeliveryCarrierColissimo(models.Model):
    _inherit = 'delivery.carrier'

    is_colissimo = fields.Boolean(compute='_compute_is_colissimo')
    colissimo_brand = fields.Char(string='Brand Code', default='BDTEST  ', groups="base.group_system")
    colissimo_packagetype = fields.Char(default="24R", groups="base.group_system")  # Advanced

    @api.depends('product_id.default_code')
    def _compute_is_colissimo(self):
        for c in self:
            c.is_colissimo = c.product_id.default_code == "CLS"

    def fixed_get_tracking_link(self, picking):
        return self.base_on_rule_get_tracking_link(picking)

    def base_on_rule_get_tracking_link(self, picking):
        if self.is_colissimo:
            return 'https://www.mondialrelay.com/public/permanent/tracking.aspx?ens=%(brand)s&exp=%(track)s&language=%(lang)s' % {
                'brand': picking.carrier_id.colissimo_brand,
                'brand': picking.carrier_id.colissimo_brand,
                'track': picking.carrier_tracking_ref,
                'lang': (picking.partner_id.lang or 'fr').split('_')[0],
            }
        return super().based_on_rule_get_tracking_link(picking)
