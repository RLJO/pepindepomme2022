# -*- coding: utf-8 -*-
# Copyright 2021 CTO IT Consulting
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo import models, fields, api, exceptions, _
from odoo.addons.prestashop_connector_gt.prestapyt.prestapyt import PrestaShopWebService as PrestaShopWebService
from odoo.addons.prestashop_connector_gt.prestapyt.prestapyt import PrestaShopWebServiceDict as PrestaShopWebServiceDict

class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    presta_id = fields.Integer(
        string='Prestashop ID',
        index=True,
        copy=False,
        default=False,
        readonly=True)

    @api.model
    def create(self, vals):
        new = super(ProductAttributeValue, self).create(vals)
        new.create_prestashop(new)
        return new

    @api.model
    def create_prestashop(self, value):
        shop = self.env['sale.shop'].search([])
        prestashop = PrestaShopWebServiceDict(shop.shop_physical_url,shop.prestashop_instance_id.webservice_key or None)
        product_schema = prestashop.get('product_option_values', options={'schema': 'blank'})
        self._fill_prestashop_data(product_schema, value)
        res = prestashop.add('product_option_values', product_schema)
        self.presta_id = int(res.get('prestashop').get('product_option_value').get('id'))

    def _fill_prestashop_data(self, data, value):
        if not value.attribute_id.presta_id:
            raise exceptions.ValidationError(_(
                'The attribute not exist in prestahop, maybe first create only the attribute'))
        data.get('product_option_value').update({
            'value': value.name,
            'id_attribute_group':int(value.attribute_id.presta_id)
        })
        data.get('product_option_value').get('name').get('language').update({
            'value':value.name
        })
    