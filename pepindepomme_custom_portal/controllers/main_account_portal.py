# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class MainPortal(http.Controller):

    @http.route(['/my/history', '/my/history/page/<int:page>'], type='http', auth="user", website=True)
    def get_history(self, page=0, search='', **kw):
        partner_id =request.env.user.partner_id.id
        documents = request.env['ir.attachment'].search([('res_id','=',partner_id),('res_model','=','res.partner')])

        return request.render("pepindepomme_custom_portal.history",{"documents":documents})



    @http.route(['/my/adress', '/my/adress/page/<int:page>'], type='http', auth="user", website=True)
    def get_childs(self, page=0, search='', **kw):
        values, errors = {}, {}
        values = kw
        success = False
        if ('success' in kw):
            success = "Votre adresse livraison a été bien ajouté"
        elif ('success2' in kw):
            success = "Votre adresse a été bien modifié"
        error = False
        partner_id = request.env.user.partner_id
        if ('action' in kw and kw['action'] == 'remove'):
            child = partner_id.child_ids.filtered(lambda r: r.id == int(kw['ship']))
            if (child):
                try:
                    a = False
                    try:
                        a = child.unlink()
                        request.env.cr.commit()
                        if (a):
                            success = "L'adresse a bien été supprimé."
                    except Exception as e:
                        a = child.write({"active": False})
                        request.env.cr.commit()
                        if (a):
                            success = "L'adresse a bien été supprimé."

                except Exception as e:
                    _logger.info("error %s " % (e))

                finally:
                    if (not a):
                        error = "Une erreur survenue ! veuillez réessayer !"





        nombre_de_contacts = request.env['res.partner'].search_count([('parent_id', '=', partner_id.id)])
        pager = request.website.pager(
            url="/my/adress",
            total=nombre_de_contacts,
            page=page,
            step=3,
        )
        childs = request.env['res.partner'].search([('parent_id', '=', partner_id.id)], limit=10
                                                   , offset=page)
        values = {
            'pager': pager,
            'adress': childs,
            'success': success,
            'error': error,

        }
        return request.render("pepindepomme_custom_portal.adress", values)

    @http.route(['/my/add_adress'], type='http', auth="public", website=True, sitemap=False)
    def add_adress(self, **kw):
        errors = {}, {}
        values = kw
        success = False
        error = False
        partner_id = request.env.user.partner_id.id

        countries = request.env["res.country"].search([])
        if ('submitted' in kw):
            try:
                name = kw.get('name')
                yyy = request.env['res.partner'].sudo().create(
                    {'parent_id': partner_id, 'name': name, 'phone': kw.get('tele'),
                     'street': kw.get('adresse'), 'street2': kw.get('complement_adress'),
                     'country_id': int(kw.get('country_id')),
                     'zip': kw.get('code_post'),
                     'city': kw.get('ville'), 'type': 'delivery',
                     'email': kw.get('email'), })
                success = 'Votre adresse livraison %s a été ajouté avec succes !' % (name)

                request.env.cr.commit()
                return request.redirect('/my/adress?success')
            except Exception as e:
                request.env.cr.rollback()

                error = 'Une erreur survenu ! veuillez reessayer!'

        render_values = {

            'checkout': values,
            'success': success,
            'error': error,
            'countries': countries
        }
        return request.render("pepindepomme_custom_portal.add_adress", render_values)

    @http.route(['/my/edit_adress'], type='http', auth="public", website=True, sitemap=False)
    def edit_adress(self, **kw):
        type=False
        values = kw
        success = False
        error = False
        partner_id = request.env.user.partner_id
        country = 'country_id' in values and values['country_id'] != '' and request.env['res.country'].browse(
            int(values['country_id']))
        if (country):
            country = country.id
        countries = request.env["res.country"].search([])
        child = False
        ship = ""
        mode = kw['mode'] if 'mode' in kw else ''
        if ('ship' in kw and kw['ship'] != '' and mode == "shipping"):
            ship = kw['ship']
            child = partner_id.child_ids.filtered(lambda r: r.id == int(kw['ship']))
            type='invoice'
        elif (mode == "biling"):
            child = partner_id
            type='delivery'
        if ('submitted' in kw and child):
            try:
                write = request.env['res.partner'].browse(child.id).sudo().write(
                    {'name': kw.get('name'), 'phone': kw.get('tele'),
                     'street': kw.get('adresse'), 'street2': kw.get('complement_adress'),
                     'zip': kw.get('code_post'),
                     'city': kw.get('ville'), 'type': type, 'country_id': country,
                     'email': kw.get('email'), })
                request.env.cr.commit()
                return request.redirect('/my/adress?success2')


            except:
                request.env.cr.rollback()
                error = 'Une erreur survenu ! veuillez réessayer!'
        elif (child):
            values = {'name': child.name, 'tele': child.phone, 'adresse': child.street, 'email': child.email,
                      'complement_adress': child.street2, 'code_post': child.zip, 'ville': child.city,
                      'country_id': child.country_id.id}

        render_values = {
            'checkout': values,
            'success': success,
            'error': error,
            'ship': ship,
            'countries': countries,
            'mode': kw['mode'] if 'mode' in kw else ''}
        return request.render("pepindepomme_custom_portal.edit_adress", render_values)
