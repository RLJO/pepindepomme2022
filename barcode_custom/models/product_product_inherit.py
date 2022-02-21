# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    barcode_custom = fields.Char('Barcode Custom', copy=False, help="Barcode used for packaging identification. Scan this packaging barcode from a transfer in the Barcode app to move all the contained units")


    @api.model
    def create(self, values):
        if('barcode' in values):
            values['barcode_custom']=values['barcode']
            values['barcode']=False
        res = super(ProductTemplateInherit, self).create(values)
        return res

    def write(self, values):
        if('barcode' in values):
            values['barcode_custom']=values['barcode']
            values['barcode']=False
        res = super(ProductTemplateInherit, self).write(values)
        return res

class ProductProductInherit(models.Model):
    _inherit = 'product.product'

    barcode_custom = fields.Char('Barcode Custom', copy=False, help="Barcode used for packaging identification. Scan this packaging barcode from a transfer in the Barcode app to move all the contained units")



    @api.model
    def create(self, values):
        if('barcode' in values):
            values['barcode_custom']=values['barcode']
            values['barcode']=False
        res = super(ProductProductInherit, self).create(values)
        return res

    def write(self, values):
        if('barcode' in values):
            values['barcode_custom']=values['barcode']
            values['barcode']=False
        res = super(ProductProductInherit, self).write(values)
        return res
