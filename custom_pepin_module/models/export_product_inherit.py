from odoo import api, fields, models, _
from odoo.exceptions import  UserError,RedirectWarning, ValidationError ,Warning

import logging
_logger = logging.getLogger(__name__)


class ExportPrestashopProductsInherit(models.TransientModel):
    _inherit = ['export.templates']

    def _get_store_product_presta_id(self, prestashop, erp_id):
        mapping_obj = self.env['channel.template.mappings']
        domain = [('odoo_template_id', '=', erp_id.id)]
        check = self.channel_id._match_mapping(
            mapping_obj,
            domain,
            limit=1
        )
        if(check):
            return check.store_product_id

    def prestashop_export_template(self, prestashop, channel_id, product_bs, template_record):
        cost = template_record.standard_price
        similar = template_record.alternative_product_ids
        similar_id = []
        similar_id_set = set()
        default_code = template_record.default_code or ''
        erp_category_id = template_record.public_categ_ids[0]
        presta_default_categ_id = self._get_store_categ_id(
            prestashop, erp_category_id)
        ps_extra_categ = []
        extra_categories_set = set()
        extra_categories = template_record.channel_category_ids
        extra_categories = extra_categories.filtered(lambda x: x.instance_id.id == channel_id.id)
        if extra_categories:
            for extra_category in extra_categories:
                for categ in extra_category.extra_category_ids:
                    cat_id = self._get_store_categ_id(prestashop, categ)
                    if cat_id not in extra_categories_set:
                        extra_categories_set.add(cat_id)
                        ps_extra_categ.append({'id': str(cat_id)})

        product_bs['product'].update({
            'price': str(round(template_record.with_context(pricelist=channel_id.pricelist_name.id).price, 2)),
            'active': '1',
            'weight': str(template_record.weight) or '',
            'redirect_type': '404',
            'minimal_quantity': '1',
            'available_for_order': '1',
            'show_price': '1',
            'depth': str(template_record.wk_length) or '',
            'width': str(template_record.width) or '',
            'height': str(template_record.height) or '',
            'state': '1',
            'ean13': template_record.barcode or '',
            'reference': default_code or '',
            'out_of_stock': '2',
            'condition': 'new',
            'id_category_default': str(presta_default_categ_id)
        })
        _logger.info("uuuuuuuuuuueeeeeeeeeeeeessss")
        _logger.info("%s" %(product_bs))
        if cost:
            product_bs['product']['wholesale_price'] = str(round(cost, 3))
        if type(product_bs['product']['name']['language']) == list:
            for i in range(len(product_bs['product']['name']['language'])):
                product_bs['product']['name']['language'][i]['value'] = template_record.name
                product_bs['product']['link_rewrite']['language'][i]['value'] = channel_id._get_link_rewrite(
                    '', template_record.name)
                product_bs['product']['description']['language'][i]['value'] = template_record.website_description or ""
                product_bs['product']['description_short']['language'][i]['value'] = template_record.description or ""
        else:
            product_bs['product']['name']['language']['value'] = template_record.name
            product_bs['product']['link_rewrite']['language']['value'] = channel_id._get_link_rewrite(
                '', template_record.name)
            product_bs['product']['description']['language']['value'] = template_record.website_description or ""
            product_bs['product']['description_short']['language']['value'] = template_record.description or ""
        if 'category' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['category']['id'] = str(
                presta_default_categ_id)
        if 'categories' in product_bs['product']['associations']['categories']:
            product_bs['product']['associations']['categories']['categories']['id'] = str(
                presta_default_categ_id)
        # add accessories
        if(similar):
            for s in similar:
                product_id = self._get_store_product_presta_id(prestashop, s)
                _logger.info("get store %s : %s" %(s,product_id))
                if product_id not in similar_id_set:
                    similar_id_set.add(product_id)
                    similar_id.append({'id': str(product_id)})
            product_bs['product']['associations']['accessories']['product'] = similar_id
        _logger.info('sililaaaaaaaaaaaaaaaaar ')
        _logger.info(product_bs)

        product_bs['product']['associations'].pop(
            'combinations', None)
        product_bs['product']['associations'].pop('images', None)
        product_bs['product'].pop('position_in_category', None)
        product_bs['product'].pop('manufacturer_name', None)

        if ps_extra_categ:
            if 'category' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['category'] = ps_extra_categ
            if 'categories' in product_bs['product']['associations']['categories']:
                product_bs['product']['associations']['categories']['categories'] = ps_extra_categ
        try:
            returnid = prestashop.add('products', product_bs)
        except Exception as e:
            _logger.info("Error in creating Product Template : %r", str(e))
            if channel_id.debug in ["enable"]:
                raise UserError(f"Error in creating Product Template : {e}")
            return [False, ""]
        return [True, returnid]