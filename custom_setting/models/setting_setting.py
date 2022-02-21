# Copyright 2016-2017 Akretion (http://www.akretion.com)
# Copyright 2016-2017 Camptocamp (http://www.camptocamp.com/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
import logging
import pandas as pd
from PIL import Image,ImageColor
import urllib.request, ssl, base64

_logger = logging.getLogger(__name__)


class setting_setting_amb(models.TransientModel):
    _name = 'setting.setting'
    _description = 'Setting'

    url_upload = fields.Char("Url")

    def publier_product(self):
        for record in self.env['product.template'].sudo().search([]):
            record.is_published = True
        return True
    def unlink_extra_category(self):
        category = self.env['extra.categories'].search([])
        category.unlink()
        return True


    def delete_extra_category(self):
        products = self.env['product.template'].search([('active', 'in', (False, True)),('channel_category_ids','!=',False)])
        for p in products:
            p.channel_category_ids=[(5)]
        return True
    def update_extrat_category(self):
        products = self.env['product.template'].search([('active','in',(False,True))])
        for product in products:
            product.change_extra_categ()
        return True


    def update_categ(self):
        _logger.info("deeeeeeeeeeeeeeeeeeeeeebbb")
        categories =self.env['product.public.category'].sudo().search([])
        for record in self.env['product.template'].sudo().search([]):
            if record.channel_category_ids:
                if record.channel_category_ids[0].extra_category_ids:
                    for m in record.channel_category_ids[0].extra_category_ids:
                        #raise UserError("categorie %s product %s" %(m,record))
                        vr = categories.filtered(lambda r: r.display_name==m.display_name)
                        if vr and len(vr)==1:
                            #continue
                            record.public_categ_ids = [(4, vr.id)]
                        else:
                            _logger.info("errreeeeeur %s produit %s categories : %s" %(m,record,vr))

    def update_description(self):
        for record in self.env['product.template'].sudo().search([('description_sale','!=',False)]):
            desc=record.description_sale
            record.write({'website_description':desc,'description_sale':False})
        return True

    def update_product_category(self):
        categories = self.env['product.category'].search([('active', 'in', (True, False))])
        for c in categories:
            c.write({'active': True})
        return True

    def update_attribute(self):
        attrs = self.env['product.attribute'].search([])
        for att in attrs:
            att.write({'create_variant': 'dynamic'})
        return True

    def create_product_prestashop(self):
        url = self.url_upload
        #df = pd.read_excel(url)
        list = url.split(";")
        ar = []
        for i in list:
            try:
                id_prest = int(i)
                template = self.env['import.operation'].create({
                    "channel_id": 1,
                    "operation": "import",
                    "object":"product.template",
                    "prestashop_filter_type":"by_id",
                    "prestashop_object_id":id_prest
                }).import_button()
                #template.unlink()
            except Exception as e:
                #self.env.cr.rollback()
                _logger.warn("erreeeeeeeeeeeur %s" %(e))


    def check_data(self):
        df1 = pd.read_excel("/home/odoo/src/user/custom_setting/models/odoo.xlsx")
        df2 = pd.read_excel("/home/odoo/src/user/custom_setting/models/presta.xlsx")
        _logger.info("débuuuuuuuuuuuuuuuuuuuut ")
        for i, row in df1.iterrows():
            a = row.to_dict()
            id=a['Product ID']
            for j, row2 in df2.iterrows():
                c = row2.to_dict()
                if(id==c['id_product']):
                    count=c['count']
                    product = self.env['channel.template.mappings'].search([('store_product_id','=',id)])
                    if(not product):
                        _logger.info("not product store id %s" %(id))
                        break
                    else:
                        temp_odoo =self.env['product.template'].browse(int(product.odoo_template_id))
                        variant = len(temp_odoo.product_variant_ids)
                        if(variant != count):
                            _logger.info("errreeeur count %s : %s" %(id,temp_odoo.id))
                    break
        _logger.info("fiiiiiiiiiiiiiiiiiiiiiiiin")
    def update_att_value(self):

        import numpy as np
        _logger.info("deeeeeeeeeeeeeeeeeeeb")
        context = ssl._create_unverified_context()
        df = pd.read_excel("/home/odoo/src/user/custom_setting/models/liste_import_value.xlsx")
        count=0
        count2=0
        count3 =0
        for i, row in df.iterrows():
            data={}
            a = row.to_dict()
            url = a['url_image']
            couleur = a['color'] if str(a['color']) not in ("nan",""," ") else False
            try:
                request = urllib.request.Request(url)
                response = urllib.request.urlopen(request, context=context)
                data_content = response.read()
                ImageBase64 = base64.b64encode(data_content)
                str_image = ImageBase64.decode('ascii')
                data['dr_image']=str_image
                _logger.info("foouuuuund")
                count3 +=1

            except Exception as e:
                _logger.info("erreur %s" %e)
                data['dr_image'] = False
            finally:
                id_value_presta = a['id_attribute']
                id_value_odoo = self.env['channel.attribute.value.mappings'].search(
                    [('store_attribute_value_id', '=', str(id_value_presta))])
                if (id_value_odoo):
                    count += 1
                    #value = self.env['product.attribute.value'].browse(int(id_value_odoo.odoo_attribute_value_id))
                    data['html_color'] = couleur
                    id_value_odoo.attribute_value_name.write(data)
        _logger.info("count : %s , count2 %s , count3 :%s" %(count,count2,count3))
        _logger.info("fiiiiiiiiiiiiiiiiiiiiiin")
        return True
    def check_value(self):
        values = self.env['product.attribute.value'].search([('html_color','!=',False),('dr_image','!=',False)])
        _logger.info("Nombre qui ont 2 champs : %s" %(len(values)))
        _logger.info("LEs valeurs : %s" %(values))
        _logger.info("les ids %s "%(values.ids))
        return True

    def create_image(self):
        from io import BytesIO
        values = self.env['product.attribute.value'].search([('html_color','!=',False),('dr_image','=',False)])
        for v in values :
            _logger.info("creeeeeeeeeeeeeeeeeeation image ")
            _logger.info(v)
            _logger.info(v.html_color)
            img = Image.new("RGB", (27, 27), ImageColor.getrgb(v.html_color))
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue())
            # _logger.info(img)
            v.write({'dr_image':img_str})

        return True











    def updte_custom_barcode(self):
        template=self.env['product.template'].search([])
        for t in template:
            code= t.barcode
            t.write({'barcode_custom':code,'barcode':False})
        return  False





