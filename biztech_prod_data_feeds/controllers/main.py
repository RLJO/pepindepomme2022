# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and
# licensing details.


from odoo.http import request
from odoo import http, models, _
from collections import OrderedDict
import hashlib
import re
import json
import jxmlease
import sys
from imp import reload
reload(sys)
# sys.setdefaultencoding('utf-8')


python3 = sys.version_info >= (3, 0)
if python3:
    unicode = str

list_of_main_tags = []
dynamic_val1 = {}
re_list = None


class GenerateFeeds(models.Model):
    _name = 'generatefeeds.live.feeds'
    _description = ' GenerateFeeds Live'

    def my_image_url(self, record, field, size=None):
        """ Returns a local url that points to the image field of a given browse record. """
        sudo_record = record.sudo()
        sha = hashlib.sha1(str(getattr(sudo_record, '__last_update')
                               ).encode('utf-8')).hexdigest()[0:7]
        size = '' if size is None else '/%s' % size
        return '/web/image/%s/%s/%s%s?unique=%s' % (record._name, record.id, field, size, sha)

    def my_compute_price(self, variant, pricelist):
        price = list(pricelist.sudo().price_rule_get(
            variant.id, 1).values())[0][0]
        return round(price, 2)

    def store_data(self, main_dict, tag, val, parent_tag=None):
        final_val = ''
        if not val:
            val = ''
        if isinstance(val, (list)) and not re_list:
            if dynamic_val1 and dynamic_val1.get(0):
                final_val = dynamic_val1.get(0) + val[0]
            elif dynamic_val1 and dynamic_val1.get(1):
                final_val = val[0] + dynamic_val1.get(1)
            else:
                final_val = val[0]
        elif not isinstance(val, (list)) and not re_list:
            final_val = val
        elif isinstance(val, (list)) and re_list:
            val.reverse()
            for rec in re_list:
                if rec[1]:
                    final_val += str(rec[1])
                else:
                    final_val += str(val.pop())
        else:
            final_val = str(val)
        if parent_tag:
            if isinstance(main_dict, (dict)) and not main_dict.get(parent_tag):
                main_dict[parent_tag] = [OrderedDict()]
            if list_of_main_tags.count(parent_tag) > len(main_dict[parent_tag]):
                main_dict[parent_tag].append(OrderedDict())

            if isinstance(main_dict[parent_tag][-1:][0], (dict)):
                if isinstance(main_dict[parent_tag][-1:][0], (dict)):
                    main_dict[parent_tag][-1:][0].update({
                        tag: final_val
                    })
                else:
                    self.store_data(main_dict[parent_tag][
                                    list_of_main_tags.count(parent_tag)-1], tag, val)

            if isinstance(main_dict[parent_tag][0], (unicode)):
                main_product_dict_list = [rec for rec in main_dict[
                    parent_tag] if isinstance(rec, (dict))]
                if list_of_main_tags.count(parent_tag) > len(main_product_dict_list):
                    main_dict[parent_tag].append(OrderedDict())
                if isinstance(main_dict[parent_tag][-1:][0], (dict)):
                    main_dict[parent_tag][-1:][0].update({
                        tag: final_val
                    })

        else:
            if isinstance(main_dict, dict) and not main_dict.get(tag):
                main_dict[tag] = []

            if isinstance(main_dict, dict):
                main_dict[tag].append(final_val)
        return main_dict

    def generate_live_feeds(self, feed):
        values = {}
        values['feed'] = feed
        prod_temp_obj = self.env['product.template']

        values['base_url'] = self.env[
            'ir.config_parameter'].sudo().get_param('web.base.url')
        values['prod_data_feeds'] = []
        if feed and feed.product_ids and feed.feed_selection == 'product':
            values['prod_data_feeds'] = prod_temp_obj.sudo().search(
                [('sale_ok', '=', True), ('id', 'in', feed.product_ids.ids)])
        if feed and feed.product_category_ids and feed.feed_selection == 'category':
            values['prod_data_feeds'] = prod_temp_obj.sudo().search(
                [('sale_ok', '=', True), ('categ_id', 'in', feed.product_category_ids.ids)])
        if feed and feed.product_public_categ_ids and feed.feed_selection == 'web_category':
            values['prod_data_feeds'] = prod_temp_obj.sudo().search(
                [('sale_ok', '=', True), ('public_categ_ids', 'in', feed.product_public_categ_ids.ids)])

        dlist = []
        full_final_prod_dict = {}
        collections_field_with_type = []
        if not values.get('base_url'):
            values['base_url'] = 'http://127.0.0.1:8069'

        # for field_name, field in prod_temp_obj._fields.iteritems():
        for field_name, field in prod_temp_obj._fields.items():
            product_data = {}
            field_type = prod_temp_obj._fields.get(field_name)
            product_data[field_name] = field_type.type
            collections_field_with_type.append(product_data)

        default_lang = ''
        if feed.feed_lang_id:
            default_lang = feed.feed_lang_id.code
        else:
            default_lang = 'en_US'
        assign_parent = feed.assign_parent_tag
        for product in values['prod_data_feeds']:
            d = OrderedDict()
            start_main_tag = ""
            global list_of_main_tags
            global dynamic_val1
            list_of_main_tags = []
            first_line = feed.product_pattern.split('\n')[0]
            # use to make parent having only words like "<item>"
            if re.search('>(.*)', first_line) and re.search('>(.*)', first_line).group(1) == '':
                assign_parent = re.search('<(.*)>', first_line).group(1)
            for final in feed.product_pattern.split('\n'):
                if final:
                    starting = ending = tag_value = None
                    starting_sqr = tag_value_sqr = tag_value_replica = None
                    if not re.search('<(.*)>\(', final):
                        if re.search('<(.*)>{', final):
                            starting = re.search('<(.*)>{', final).group(1)
                        if re.search('{(.*)}', final):
                            tag_value = re.search('{(.*)}', final).group(1)
                            if tag_value and re.search('(.*)}\[', final):
                                tag_value_replica = re.search('\[(.*)\]', final).group(1)
                    # use to define static website with dynamic data like ([static]{dynamic})
                    # or ({dynamic}[static])
                    dynamic_link_tag = dynamic_val2 = None
                    dynamic_val1 = {}
                    if re.search('<(.*)>\(', final):
                        starting = re.search('<(.*)>\(', final).group(1)

                        # finding th sequece for placing static data after or before the actual value
                        # --------------start finding sequence------------------------
                        if re.search('\(\[(.*)\]', final):
                            dynamic_val1[0] = re.search('\[(.*)\]', final).group(1)
                        if re.search('\[(.*)\]\)', final):
                            dynamic_val1[1] = re.search('\[(.*)\]', final).group(1)
                        if re.search('{(.*)}', final):
                            tag_value = re.search('{(.*)}', final).group(1)
                        # --------------end finding sequence------------------------

                    if re.search('<(.*)>\[', final):
                        starting_sqr = re.search('<(.*)>\[', final).group(1)
                    if re.search('\[(.*)\]', final):
                        tag_value_sqr = re.search('\[(.*)\]', final).group(1)
                    # use main tag to make it parent and all data tags after
                    # it can consider as child till ending main tag was not fount
                    main_tag_data = re.search('<(\w+):(\w+)>', final)
                    if main_tag_data:
                        rest_data = re.search('>(.*)', final)
                        main_tag_data = re.search('<(.*)>', final).group(1)
                        if rest_data and rest_data.group(1) == '' and main_tag_data != assign_parent:
                            start_main_tag = main_tag_data
                            list_of_main_tags.append(str(start_main_tag))
                    if re.search('<(.*)>', final) and start_main_tag:
                        if re.search('<(.*)>', final) and re.search('<(.*)>', final).group(1)[0] == '/':
                            start_main_tag = ''

                    main_tag_data = re.search('<(\w+)>', final)
                    if main_tag_data:
                        rest_data = re.search('>(.*)', final)
                        main_tag_data = re.search('<(.*)>', final).group(1)
                        if rest_data and rest_data.group(1) == '' and main_tag_data != assign_parent:
                            start_main_tag = main_tag_data
                            list_of_main_tags.append(str(start_main_tag))
                    if re.search('<(.*)>', final) and start_main_tag:
                        if re.search('<(.*)>', final) and re.search('<(.*)>', final).group(1)[0] == '/':
                            start_main_tag = ''

                    my_domain = False
                    tag_name = False
                    if tag_value and tag_value.find('.') != -1:
                        val = tag_value.split('.')
                        my_domain = val[0]
                        tag_value = val[1]

                    if tag_value and tag_value.find(':') != -1:
                        val = tag_value.split(':')
                        tag_name = val[0]
                        tag_value = val[1]
                    if not starting and starting_sqr and tag_value_sqr:
                        self.store_data(main_dict=d,
                                        tag=starting_sqr,
                                        parent_tag=start_main_tag,
                                        val=tag_value_sqr)
    ##########################################################################
                    tag_val_list = []
                    global re_list
                    re_list = None
                    if re.search('<(.*)>\(', final):
                        re_list = re.findall(r"(\[([^][]+)\]|\{([\w+.:]+)\})", str(final))
                        if re_list:
                            for rec in re_list:
                                if rec[2] != '':
                                    fin_val = rec[2].split(
                                        '.')[-1:][0] if rec[2].find('.') else rec[2]
                                    fin_val = rec[2].split(
                                        ':')[-1:][0] if rec[2].find(':') else rec[2]
                                    tag_val_list.append(fin_val)

                    if starting and tag_value and not starting_sqr:
                        if not tag_val_list:
                            tag_val_list.append(tag_value)
                        lsd = []
                        for tag_value in tag_val_list:
                            val = ''
                            if tag_value and tag_value.find('.') != -1:
                                val = tag_value.split('.')
                                my_domain = val[0]
                                tag_value = val[1]
                            if tag_name != 'variants':
                                field_val = None
                                # use when the product field does not exists
                                if hasattr(product, tag_value):
                                    field_val = product.read([tag_value])[0]
                                else:
                                    val = tag_value_replica if tag_value_replica else ''

                                for field_and_type in collections_field_with_type:
                                    if tag_value == list(field_and_type.keys())[0]:
                                        if field_and_type.get(tag_value) in ['char', 'text', 'float', 'integer', 'selection', 'boolean', 'date', 'datetime', 'html']:
                                            if not my_domain:
                                                if tag_value in ('lst_price', 'list_price', 'standard_price'):
                                                    final_price = []
                                                    for prod in self.env['product.product'].sudo().search([('product_tmpl_id', '=', product.id)]):
                                                        final_price.append(
                                                            self.my_compute_price(prod, feed.pricelist_id))
                                                    val = str(json.dumps(
                                                        list(final_price))).strip('[]')

                                                if tag_value not in ('lst_price', 'list_price', 'standard_price'):
                                                    if field_val.get(tag_value):
                                                        # import sys
                                                        # reload(sys)
                                                        # sys.setdefaultencoding('utf-8')
                                                        convert_string = str(
                                                            field_val.get(tag_value))
                                                        self.env.cr.execute('select value from ir_translation where lang=%s and type=%s and src like %s;', (
                                                            default_lang, 'model', (convert_string or u'').strip()))  # .encode('utf-8')))
                                                        res_trans = self.env.cr.fetchone()

                                                        if field_and_type.get(tag_value) in ['html']:
                                                            if res_trans and res_trans[0]:
                                                                element = re.sub(
                                                                    '<[A-Za-z\/][^>]*>', '', res_trans[0])
                                                                val = element if element else ''
                                                            else:
                                                                res = field_val.get(
                                                                    tag_value)
                                                                element = re.sub(
                                                                    '<[A-Za-z\/][^>]*>', '', res)
                                                                val = element if element else ''
                                                        else:
                                                            if res_trans:
                                                                val = res_trans[
                                                                    0] if res_trans[0] else ''
                                                            else:
                                                                val = field_val.get(tag_value) if field_val.get(
                                                                    tag_value) else ''
                                                    else:
                                                        replica_val = tag_value_replica if tag_value_replica else field_val.get(
                                                            tag_value)
                                                        val = replica_val

                                            if my_domain:

                                                if field_val.get(tag_value):
                                                    if values['base_url'][-1:] != '/' and field_val.get(tag_value)[0] != '/':
                                                        base_val = str(
                                                            values['base_url']) + '/' + str(field_val.get(tag_value))
                                                        val = base_val
                                                    else:
                                                        base_val = values[
                                                            'base_url'] + field_val.get(tag_value)
                                                        val = base_val
                                                else:
                                                    base_val = values['base_url'] + \
                                                        field_val.get(tag_value)
                                                    val = base_val

                                        if field_and_type.get(tag_value) == 'binary':
                                            product_image = self.my_image_url(
                                                product, 'image_1920',)
                                            if not my_domain:
                                                val = product_image
                                            if my_domain:
                                                val = values['base_url'] + \
                                                    product_image

                                        if field_and_type.get(tag_value) == 'many2one':
                                            if field_val.get(tag_value) and len(field_val.get(tag_value)) >= 2:
                                                if '/' in field_val.get(tag_value)[1]:
                                                    res_trans_pack = []
                                                    for trans in field_val.get(tag_value)[1].split('/'):
                                                        self.env.cr.execute('select value from ir_translation where lang=%s and src like %s;', (
                                                            default_lang, str(trans.strip())))  # .encode('utf-8'))))
                                                        dataa = self.env.cr.fetchone()
                                                        if dataa:
                                                            res_trans_pack.append(
                                                                dataa)
                                                    if res_trans_pack:
                                                        val = ' / '.join(t[0]
                                                                         for t in res_trans_pack if t)
                                                    else:
                                                        val = field_val.get(
                                                            tag_value)[1]
                                                else:
                                                    self.env.cr.execute('select value from ir_translation where lang=%s and type=%s and src like %s;', (
                                                        default_lang, 'model', str(field_val.get(tag_value)[1])))  # .encode('utf-8'))))
                                                    res_trans = self.env.cr.fetchone()
                                                    if res_trans:
                                                        val = res_trans[0]
                                                    else:
                                                        if field_val.get(tag_value):
                                                            val = field_val.get(
                                                                tag_value)[1]
                                                        else:
                                                            val = ''
                                            else:
                                                if tag_value_replica:
                                                    val = tag_value_replica
                                                else:
                                                    val = ''
                                        if field_and_type.get(tag_value) in ['one2many', 'many2many']:
                                            fields_obj = self.env[
                                                'ir.model.fields']
                                            field_value = fields_obj.sudo().search(
                                                [('model', '=', 'product.template'), ('name', '=', tag_value)])
                                            records = self.env[field_value.relation].sudo().search(
                                                [('id', 'in', field_val.get(tag_value))])
                                            data = []
                                            for rec in records:
                                                if rec._rec_name and rec._rec_name == 'name':
                                                    if rec.name:
                                                        if isinstance(rec.name, unicode):
                                                            self.env.cr.execute('select value from ir_translation where lang=%s and type=%s and src like %s;', (
                                                                default_lang, 'model', str(rec.name)))  # .encode('utf-8'))))
                                                            res_trans = self.env.cr.fetchone()
                                                            if type(res_trans) is tuple:
                                                                res_trans = res_trans[0]
                                                            if res_trans:
                                                                data.append(
                                                                    res_trans)
                                                            else:
                                                                data.append(
                                                                    rec.name)
                                                        else:
                                                            self.env.cr.execute('select value from ir_translation where lang=%s and type=%s and src like %s;', (
                                                                default_lang, 'model', str(rec.name.name)))  # .encode('utf-8'))))
                                                            res_trans = self.env.cr.fetchone()
                                                            if res_trans:
                                                                data.append(
                                                                    res_trans)
                                                            else:
                                                                data.append(
                                                                    rec.name.name)
                                            val = ', '.join(set(data))
                                            if not data:
                                                if tag_value_replica:
                                                    val = tag_value_replica

                            if tag_name == 'variants':
                                if len(product.product_variant_ids) > 1:
                                    variantss = []
                                    for variant in product.product_variant_ids:
                                        for var in variant.attribute_line_ids.search([('product_tmpl_id', '=', product.id), ('attribute_id.name', 'ilike', _(tag_value))]):
                                            if var.value_ids:
                                                for v in var.value_ids:
                                                    self.env.cr.execute('select value from ir_translation where lang=%s and type=%s and src like %s;', (
                                                        default_lang, 'model', str(v.name)))  # .encode('utf-8'))))
                                                    res_trans = self.env.cr.fetchone()
                                                    if res_trans:
                                                        variantss.append(
                                                            res_trans[0])
                                                    else:
                                                        variantss.append(
                                                            v.name)
                                    val = ', '.join(set(variantss))
                                elif tag_value_replica:
                                    val = tag_value_replica

                            lsd.append(val if val else '')
                        self.store_data(main_dict=d,
                                        tag=starting,
                                        parent_tag=start_main_tag,
                                        val=lsd)
                    else:
                        # use to make an empty tag visible in xml like ex.: <g:id></g:id>
                        check_empty_tag = re.search('<(.*)><(.*)', str(final).replace(' ', ''))
                        if check_empty_tag and check_empty_tag.group(1) and check_empty_tag.group(2)[0] == '/':
                            empty_val_tag = check_empty_tag.group(1)
                            self.store_data(main_dict=d,
                                            tag=empty_val_tag,
                                            parent_tag=start_main_tag,
                                            val='')
            dlist.append(d)
        if all(d for d in dlist):
            if feed.sudo().extension == 'csv':
                keys, values_data = [], []
                data = ''
                for datalist in dlist:
                    for key, value in dict(datalist).items():
                        if key not in keys:
                            keys.append(str(key))
                        values_data.append(value)
                i = 0
                data = str(keys)[1:-1]
                data = data + "\n"
                for val in values_data:
                    if i % len(keys) == 0 and i != 0:
                        data = data[:-1] + '\n'
                    for v in val:
                        v = str(v).replace(",", "|")
                        data = data + v + ','
                    i = i+1
                feed.sudo().final_product_pattern = data[:-1].replace("'", "")
            elif feed.sudo().extension == 'txt':
                keys, values_data = [], []
                data = ''
                for datalist in dlist:
                    for key, value in dict(datalist).items():
                        if key not in keys:
                            keys.append(str(key))
                        values_data.append(value)
                i = 0
                data_title = ""
                for j in keys:
                    data_title = data_title + j + "\t"
                data = data_title
                data = data + "\n"
                for val in values_data:
                    if i % len(keys) == 0 and i != 0:
                        data = data[:-1] + '\n'
                    for v in val:
                        v = str(v).replace(",", "|")
                        data = data + v + "\t"
                    i = i+1
                feed.sudo().final_product_pattern = data[:-1].replace("'", "")
            else:
                full_final_prod_dict.update({assign_parent: dlist})
                full_final_prod = jxmlease.emit_xml(full_final_prod_dict)
                new_full_final_prod = full_final_prod.replace(
                    '<?xml version="1.0" encoding="utf-8"?>', '')
                feed.sudo().final_product_pattern = new_full_final_prod
        return values


class WebsiteDataFeedControllers(http.Controller):

    @http.route(['/feeds/<model("website.data.feeds"):feed>'], type='http', auth="public")
    def prod_data_feed(self, feed):
        feeds = request.env['generatefeeds.live.feeds'].generate_live_feeds(
            feed)
        return request.render("biztech_prod_data_feeds.biztech_prod_data_feeds", feeds, headers=[('Content-Type', 'text/xml')])
