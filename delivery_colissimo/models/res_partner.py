# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResPartnerColissimo(models.Model):
    _inherit = 'res.partner'

    is_colissimo = fields.Boolean(compute='_compute_is_colissimo')

    @api.depends('ref')
    def _compute_is_colissimo(self):
        for p in self:
            p.is_colissimo = p.ref and p.ref.startswith('CLS#')

    @api.model
    def _colissimo_search_or_create(self, data):
        ref = 'CLS#%s' % data['id']
        partner = self.search([
            ('id', 'child_of', self.commercial_partner_id.ids),
            ('ref', '=', ref),
            # fast check that address always the same
            ('street', '=', data['street']),
            ('zip', '=', data['zip']),
        ])
        if not partner:
            partner = self.create({
                'ref': ref,
                'name': data['name'],
                'street': data['street'],
                'street2': data['street2'],
                'zip': data['zip'],
                'city': data['city'],
                'country_id': self.env.ref('base.%s' % data['country_code']).id,
                'type': 'delivery',
                'parent_id': self.id,
            })
        return partner

    def _avatar_get_placeholder_path(self):
        if self.is_colissimo:
            return "delivery_colissimo/static/src/img/truck_mr.png"
        return super()._avatar_get_placeholder_path()
