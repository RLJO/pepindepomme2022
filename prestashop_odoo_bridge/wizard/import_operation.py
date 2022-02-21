# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models

class PrestashopImportOperation(models.TransientModel):
    _inherit = "import.operation"

    prestashop_object_id = fields.Char()
    prestashop_import_date_from = fields.Datetime()
    prestashop_filter_type = fields.Selection([('all', 'All'), ("by_id", "By Id"), ("by_date", "By Date")], default='all')

    def prestashop_get_filter(self):
        return dict(
            page = 0,
            prestashop_object_id=self.prestashop_object_id,
            prestashop_import_date_from=self.prestashop_import_date_from
        )