# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DeliveryCarrierInherit(models.Model):
    _inherit = 'delivery.carrier'
    icon = fields.Binary("Icon")