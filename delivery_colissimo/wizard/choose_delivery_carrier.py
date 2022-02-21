# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.tools.json import scriptsafe as json_safe
from odoo.exceptions import ValidationError

import requests

class ChooseDeliveryCarrier(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    shipping_zip = fields.Char(related='order_id.partner_shipping_id.zip')
    shipping_country_code = fields.Char(related='order_id.partner_shipping_id.country_id.code')

    is_colissimo = fields.Boolean(compute='_compute_is_colissimo')
    colissimo_last_selected = fields.Char(string="Last Relay Selected", )
    colissimo_last_selected_id = fields.Char(compute='_compute_cls_last_selected_id')
    colissimo_brand = fields.Char(related='carrier_id.colissimo_brand')
    colissimo_colLivMod = fields.Char(related='carrier_id.colissimo_packagetype')
    colissimo_allowed_countries = fields.Char(compute='_compute_cls_allowed_countries')

    #colissimo only
    colissimo_ceAddress = fields.Char(related='order_id.partner_shipping_id.street')
    colissimo_ceTown=fields.Char(related='order_id.partner_shipping_id.city')
    colissimo_ceToken=fields.Char(compute="_get_colissimo_token")

    data_holder = fields.Char(string="data_holder",  )

    @api.depends('carrier_id')
    def _get_colissimo_token(self):
        post_adress = "https://ws.colissimo.fr/widget-point-retrait/rest/authenticate.rest"
        data = {
            "login": "801808",
            "password": "Pepin1010!!"
        }
        r = requests.post(url=post_adress, data=data)
        j = r.json()

        self.colissimo_ceToken = j['token']


    @api.depends('carrier_id')
    def _compute_is_colissimo(self):
        self.ensure_one()
        self.is_colissimo = self.carrier_id.product_id.default_code == "CLS"

    @api.depends('carrier_id', 'order_id.partner_shipping_id')
    def _compute_cls_last_selected_id(self):
        self.ensure_one()
        if self.order_id.partner_shipping_id.is_colissimo:
            self.colissimo_last_selected_id = '%s-%s' % (
                self.shipping_country_code,
                self.order_id.partner_shipping_id.ref.lstrip('CLS#'),
            )
        else:
            self.colissimo_last_selected_id = ''

    @api.depends('carrier_id')
    def _compute_cls_allowed_countries(self):
        self.ensure_one()
        self.colissimo_allowed_countries = ','.join(self.carrier_id.country_ids.mapped('code')).upper() or ''

    def button_confirm(self):

        if self.carrier_id.is_colissimo:
            if not self.data_holder:
                raise ValidationError(_('Please, choose a Parcel Point'))
            data = json_safe.loads(self.data_holder)
            partner_shipping = self.order_id.partner_id._colissimo_search_or_create({
                'id': data['identifiant'],
                'name': data['nom'],
                'street': data['adresse1'],
                'street2': data['adresse2'],
                'zip': data['codePostal'],
                'city': data['localite'],
                'country_code': data['codePays'][:2].lower(),
            })
            if partner_shipping != self.order_id.partner_shipping_id:
                self.order_id.partner_shipping_id = partner_shipping
                self.order_id.onchange_partner_shipping_id()

        return super().button_confirm()
