from odoo import http
from odoo.http import request
from odoo.osv import expression


class CustomWebsiteSale(http.Controller):
    @http.route(['/liste_naissance'], type='http', auth='public', website=True, sitemap=False)
    def get_liste_naissance(self, **post):
        return request.render('pepindepomme_custom_website.liste_naissance')
    @http.route(['/premiere_commande'], type='http', auth='public', website=True, sitemap=False)
    def get_premiere_commande(self, **post):
        return request.render('pepindepomme_custom_website.premiere_commande')
    @http.route(['/valise_de_maternite'], type='http', auth='public', website=True, sitemap=False)
    def get_valise_de_maternite(self, **post):
        return request.render('pepindepomme_custom_website.valise_de_maternite')
    @http.route(['/programme_fidelite'], type='http', auth='public', website=True, sitemap=False)
    def get_programme_fidelite(self, **post):
        return request.render('pepindepomme_custom_website.programme_fidelite')
    @http.route(['/offres_speciales_et_codes_promos'], type='http', auth='public', website=True, sitemap=False)
    def get_offres_speciales(self, **post):
        return request.render('pepindepomme_custom_website.offres_speciales_et_codes_promos')
    @http.route(['/personal_shopper'], type='http', auth='public', website=True, sitemap=False)
    def get_shopper(self, **post):
        return request.render('pepindepomme_custom_website.personal_shopper')
    @http.route(['/offres_et_remises_jumeaux'], type='http', auth='public', website=True, sitemap=False)
    def get_offres_et_remises_jumeaux(self, **post):
        return request.render('pepindepomme_custom_website.offres_et_remises_jumeaux')
    @http.route(['/legal-notice'], type='http', auth='public', website=True, sitemap=False)
    def notice(self, **post):
        return request.render('pepindepomme_custom_website.legal_notice')

    @http.route(['/faq'], type='http', auth='public', website=True, sitemap=False)
    def faq(self, **post):
        return request.render('pepindepomme_custom_website.faq_custom')

    @http.route(['/echanges'], type='http', auth='public', website=True, sitemap=False)
    def get_echanges(self, **post):
        return request.render('pepindepomme_custom_website.echanges_custom')

    @http.route(['/satisfait-ou-rembourse'], type='http', auth='public', website=True, sitemap=False)
    def get_satisfait(self, **post):
        return request.render('pepindepomme_custom_website.satisfait_custom')

    @http.route(['/support-garantie'], type='http', auth='public', website=True, sitemap=False)
    def get_support(self, **post):
        return request.render('pepindepomme_custom_website.support_custom')

    @http.route(['/qui-sommes-nous'], type='http', auth='public', website=True, sitemap=False)
    def get_qsn(self, **post):
        return request.render('pepindepomme_custom_website.qsn_custom',{'res_company':request.website.company_id})

    @http.route(['/affiliation'], type='http', auth='public', website=True, sitemap=False)
    def get_affiliation(self, **post):
        return request.render('pepindepomme_custom_website.affiliation_custom')

    @http.route(['/partenaires'], type='http', auth='public', website=True, sitemap=False)
    def get_partenaire(self, **post):
        return request.render('pepindepomme_custom_website.partenaires_custom')

    @http.route(['/mode_paiement'], type='http', auth='public', website=True, sitemap=False)
    def get_mode_paiement(self, **post):
        domain = expression.AND([
            [('state', 'in', ['enabled', 'test'])],
            ['|', ('website_id', '=', False), ('website_id', '=', request.website.id)]
        ])
        acquirers = request.env['payment.acquirer'].search(domain)
        return request.render('pepindepomme_custom_website.mode_paiement_custom',{'paiements':acquirers})

    @http.route(['/mode_livraison'], type='http', auth='public', website=True, sitemap=False)
    def get_mode_livraison(self, **post):

        delivery = request.env['delivery.carrier'].sudo().search([('is_published', '=', True), ('website_id', 'in', (request.website.id,False))])
        return request.render('pepindepomme_custom_website.mode_livraison_custom',{'delivery':delivery})


