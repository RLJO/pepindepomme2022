#!/usr/bin/env python
# -*- coding: utf-8 -*-
#################################################################################
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    See LICENSE file for full copyright and licensing details.
#################################################################################

from odoo import api, fields, models, _
import re
import base64
import logging
_logger     = logging.getLogger(__name__)
from odoo.exceptions import UserError
from .prestapi import PrestaShopWebService,PrestaShopWebServiceDict,PrestaShopWebServiceError,PrestaShopAuthenticationError

Type = [
    ('simple','Simple Product'),
    ('downloadable','Downloadable Product'),
    ('grouped','Grouped Product'),
    ('virtual','Virtual Product'),
    ('bundle','Bundle Product'),
]
TaxType = [
    ('include','Include In Price'),
    ('exclude','Exclude In Price')
]
Boolean = [
    ('1', 'True'),
    ('0', 'False'),
]


class MultiChannelSale(models.Model):
    _inherit = "multi.channel.sale"

    ps_language_id = fields.Char(
        'Prestashop Language Id',
        size = 2,
        help="Enter Prestashop's Default language Id "
    )

    default_tax_type = fields.Selection(
        selection = TaxType,
        string = 'Default Tax Type',
        default = 'exclude',
        required = 1
    )
    ps_default_product_type = fields.Selection(
        selection = Type,
        string = 'Default Product Type',
        default = 'simple',
        required = 1,
        help = _("Select default product type for prestashop end.")
    )
    ps_default_tax_rule_id = fields.Char(
        string = 'Default Tax Class ID',
        default = '0',
        required = 1,
    )

    @api.model
    def get_channel(self):
        result = super(MultiChannelSale, self).get_channel()
        result.append(("prestashop", "Prestashop"))
        return result

    @api.model
    def _prestashop_get_product_images_vals(self, media):
        vals = dict()
        message = ''
        data = None
        image_url = media
        if image_url:
            prestashop = self._context['prestashop']
            try:
                data = prestashop.get(image_url)
                image_data = base64.b64encode(data)
            except Exception as e:
                message += '<br/>%s'%(e)
            else:
                vals['image'] = image_data
                return vals
        return {'image':False}

    def get_core_feature_compatible_channels(self):
        vals = super().get_core_feature_compatible_channels()
        vals.append('prestashop')
        return vals

    def connect_prestashop(self):
        message = '<b>Connection Error: </b>'
        try:
            prestashop = PrestaShopWebServiceDict(
                self.url, self.api_key)
            languages = prestashop.get("languages", options = {'filter[active]':'1'})
            if languages.get("languages",{}).get("language"):
                message = '<b> Connection successfull !!! </b>'
        except Exception as e:
            message += str(e)
            return False,message
        return True, message

#-----------------------------------------Import Process --------------------------------------------------

    def import_prestashop(self, object, **kwargs):
        kwargs.update(message = "No Records Found ...")
        prestashop = PrestaShopWebServiceDict(
            self.url, self.api_key)
        data_list = []
        if object == 'product.category':
            data_list = self.import_prestashop_categories(
                prestashop, **kwargs)
        elif object == 'res.partner':
            data_list = self.import_prestashop_customers(
                prestashop, **kwargs)
        elif object == 'product.template':
            data_list = self.import_prestashop_products(
                prestashop, **kwargs)
        elif object == 'sale.order':
            data_list = self.import_prestashop_orders(
                prestashop, **kwargs)
        elif object == "delivery.carrier":
            data_list = self.import_prestashop_shippings(
                prestashop, **kwargs)
        kwargs["page"] += kwargs.get("page_size")
        return data_list, kwargs

    def import_prestashop_products(self, prestashop, **kwargs):
        vals = dict(
            channel_id=self.id,
            operation='import',
        )
        obj = self.env['import.prestashop.products'].create(vals)
        self.env.cr.commit()
        return obj.with_context({
            "prestashop": prestashop,
        }).import_now(**kwargs)

    def import_prestashop_categories(self, prestashop, **kwargs):
        vals = dict(
            channel_id=self.id,
            operation='import',
        )
        obj = self.env['import.prestashop.categories'].create(vals)
        return obj.with_context({
            "prestashop": prestashop,
        }).import_now(**kwargs)

    def import_prestashop_customers(self, prestashop, **kwargs):
        vals = dict(
            channel_id=self.id,
            operation='import',
        )
        obj = self.env['import.prestashop.partners'].create(vals)
        return obj.with_context({
            "prestashop": prestashop,
        }).import_now(**kwargs)

    def import_prestashop_shippings(self, prestashop, **kwargs):
        vals = dict(
            channel_id=self.id,
            operation='import',
        )
        obj = self.env['import.prestashop.shipping'].create(vals)
        return obj.with_context({
            "prestashop": prestashop,
        }).import_now(**kwargs)

    def import_prestashop_orders(self, prestashop, **kwargs):
        vals = dict(
            channel_id=self.id,
            operation='import',
        )
        obj = self.env['import.prestashop.orders'].create(vals)
        return obj.with_context({
            'prestashop': prestashop,
        }).import_now(**kwargs)

#-----------------------------------------Export Process ---------------------------------------------

    def export_prestashop(self, record):
        prestashop = PrestaShopWebServiceDict(
            self.url, self.api_key)
        data_list = []
        if record._name == 'product.category':
            initial_record_id = record.id
            data_list = self.export_prestashop_categories(
                prestashop, record, initial_record_id)
        elif record._name == 'product.template':
            data_list = self.export_prestashop_products(prestashop, record)
        return data_list

    def export_prestashop_products(self, prestashop, record):
        vals = dict(
            channel_id=self.id,
            operation='export',
        )
        obj = self.env['export.templates'].create(vals)
        return obj.with_context({
            'prestashop': prestashop,
            'channel_id': self,
        }).prestashop_export_now(record)

    def export_prestashop_categories(self, prestashop, record, initial_record_id):
        vals = dict(
            channel_id=self.id,
            operation='export',
        )
        obj = self.env['export.categories'].create(vals)
        return obj.with_context({
            'prestashop': prestashop,
            'channel_id': self,
        }).prestashop_export_now(record, initial_record_id)

# ------------------------------------------Update Process ----------------------------------------------

    def update_prestashop(self, record, get_remote_id):
        prestashop = PrestaShopWebServiceDict(
            self.url, self.api_key)
        data_list = []
        if prestashop:
            remote_id = get_remote_id(record)
            if record._name == 'product.category':
                initial_record_id  = record.id
                data_list = self.update_prestashop_categories(prestashop, record, initial_record_id,remote_id)
            if record._name == 'product.template':
                data_list = self.update_prestashop_products(
                    prestashop, record, remote_id)
            return data_list

    def update_prestashop_categories(self,prestashop, record, initial_record_id,remote_id):
        vals = dict(
            channel_id=self.id,
            operation='update',
        )
        obj = self.env['export.categories'].create(vals)
        return obj.with_context({
            'prestashop': prestashop,
            'channel_id': self,
        }).prestashop_update_now(record, remote_id)

    def update_prestashop_products(self, prestashop, record, remote_id):
        vals = dict(
            channel_id=self.id,
            operation='update',
        )
        obj = self.env['export.templates'].create(vals)
        return obj.with_context({
            'prestashop': prestashop,
            'channel_id': self,
        }).prestashop_update_now(record, remote_id)

#--------------------------------------------Import crons -----------------------------------------------

    def prestashop_import_category_cron(self):
        _logger.info("+++++++++++Import Category Cron Started++++++++++++")
        kw = dict(
            object = "product.category",
            page = 0,
            from_cron = True
        )
        self.env["import.operation"].create({
            "channel_id":self.id ,
        }).import_with_filter(**kw)

    def prestashop_import_partner_cron(self):
        _logger.info("+++++++++++Import Partner Cron Started++++++++++++")
        kw = dict(
            object = "res.partner",
            page = 0,
            prestashop_import_date_from=self.import_customer_date,
            from_cron = True
        )
        self.env["import.operation"].create({
            "channel_id":self.id ,
        }).import_with_filter(**kw)

    def prestashop_import_product_cron(self):
        _logger.info("+++++++++++Import Product Cron Started++++++++++++")
        kw = dict(
            object = "product.template",
            page = 0,
            prestashop_import_date_from=self.import_product_date,
            from_cron = True,
        )
        self.env["import.operation"].create({
            "channel_id":self.id ,
        }).import_with_filter(**kw)

    def prestashop_import_order_cron(self):
        _logger.info("+++++++++++Import Order Cron Started++++++++++++")
        kw = dict(
            object = "sale.order",
            page = 0,
            prestashop_import_date_from=self.import_order_date,
            from_cron = True
        )
        self.env["import.operation"].create({
            "channel_id":self.id ,
        }).import_with_filter(**kw)

#------------------------------------------------------------------------------------------------------------

    def sync_quantity_prestashop(self, mapping, qty):
        prestashop = PrestaShopWebServiceDict(
            self.url, self.api_key)
        pres_combination_id = mapping.store_variant_id
        pres_product_id = mapping.store_product_id
        if pres_product_id == pres_combination_id:
            self.env['export.templates'].prestashop_update_quantity(prestashop,pres_product_id , qty)
        else:
            self.env['export.templates'].prestashop_update_quantity(prestashop,pres_product_id , qty,attribute_id = pres_combination_id)

    def sync_order_feeds(self, vals, **kwargs):
        for line_id in vals[0]['line_ids']:
            line_id = line_id[2]
            if line_id['line_source'] == "discount":
                line_price = line_id['line_price_unit']
                line_id['line_price_unit'] = line_price['total_discounts_tax_incl'] if self.default_tax_type == 'include'\
                    else line_price['total_discounts_tax_excl']
        res = super().sync_order_feeds(vals, **kwargs)
        return res

    def _get_link_rewrite(self, zip, string):
        if type(string) != str:
            string = string.encode('ascii','ignore')
            string = str(string)
        string = re.sub('[^A-Za-z0-9]+',' ',string)
        string = string.replace(' ', '-').replace('/', '-')
        string = string.lower()
        return string

    def prestashop_pre_cancel_order(self,sale_record, mapping_ids):
        prestashop = PrestaShopWebServiceDict(self.url, self.api_key)
        order_id = mapping_ids.store_order_id
        if order_id:
            try:
                order_his_data = prestashop.get('order_histories', options = {'schema': 'blank'})
                order_his_data['order_history'].update({
                'id_order' : order_id,
                'id_order_state' : 6
                })
                state_update = prestashop.add('order_histories', order_his_data)
            except Exception as e:
                _logger.info("Error in updating Cancellation Status ==> %r",format(str(e)))

    def prestashop_pre_confirm_paid(self, invoice, mapping_ids):
        prestashop = PrestaShopWebServiceDict(self.url, self.api_key)
        order_id = mapping_ids.store_order_id
        if order_id:
            try:
                order_his_data = prestashop.get('order_histories', options={'schema': 'blank'})
                order_his_data['order_history'].update({
                'id_order' : order_id,
                'id_order_state' : 2
                })
                state_update = prestashop.add('order_histories?sendemail=1', order_his_data)
            except Exception as e:
                _logger.info("Error in updating Paid status : %r",str(e))

    def prestashop_pre_do_transfer(self, stock_move_record, mapping_ids):
        prestashop = PrestaShopWebServiceDict(self.url, self.api_key)
        order_id = mapping_ids.store_order_id
        if order_id:
            try:
                order_his_data = prestashop.get('order_histories',
                    options={'schema': 'blank'})
                order_his_data['order_history'].update({
                'id_order' : order_id,
                'id_order_state' : 4
                })
                state_update = prestashop.add('order_histories', order_his_data)
            except Exception as e:
                _logger.info("Error in updating shipping status : %r",str(e))
