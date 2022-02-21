
# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _

class SaleShopInherit(models.Model):
    _inherit = 'sale.shop'

    active = fields.Boolean("actif")
