# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplateInherit(models.Model):
    _inherit = "product.template"


    def update_parent_cat(self):
        for rec in self:
            rec.parent_id = False
        return True

    # @api.onchange('public_categ_ids')
    # def change_extra_categ(self):
    #     for rec in self:
    #         tab = []
    #         channel_category_ids = []
    #         rec.channel_category_ids = [(5)]
    #         if (rec.public_categ_ids):
    #             for x in rec.public_categ_ids.ids:
    #                 if (type(x) == int):
    #                     tab.append((4, x))
    #         if (len(tab) > 0):
    #             channel_category_ids.append((0, 0, {'instance_id': 1, 'extra_category_ids': tab}))
    #             rec.channel_category_ids = channel_category_ids
    #     return True

