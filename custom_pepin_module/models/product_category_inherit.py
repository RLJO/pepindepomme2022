# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductPublicCategoryInherit(models.Model):
    _inherit = "product.public.category"

    active = fields.Boolean('Actif',default=True)


    def update_parent_cat(self):
        for rec in self:
            rec.parent_id = False
        return True





