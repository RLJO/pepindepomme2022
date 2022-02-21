from odoo import _, api, fields,models
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dr_brand_id = fields.Many2one('dr.product.brand', string='Brand',compute='_compute_brand',readonly=False,store=True)

    @api.depends('hs_code')
    def _compute_brand(self):
    	for r in self:
    		if r.hs_code:
    		  search = self.env['dr.product.brand'].search([('id_presta', '=', r.hs_code)])
    		  r.dr_brand_id = search.id
class ProductTemplate_brand(models.Model):
    _inherit = "dr.product.brand"
    
    id_presta = fields.Char(string='id_prestat')
