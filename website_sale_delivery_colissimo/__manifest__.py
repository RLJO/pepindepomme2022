# -*- coding: utf-8 -*-
{
    'name': "website_sale_delivery_colissimo",
    'summary': """ Let's choose Point Relais® on your ecommerce """,

    'description': """
        This module allow your customer to choose a Point Relais® and use it as shipping address.
    """,
    'category': 'Website/Website',
    'version': '0.1',
    'depends': ['web','website_sale', 'website_sale_delivery', 'delivery_colissimo'],
    'data': [
        'views/templates.xml',
        'views/assets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'website_sale_delivery_colissimo/static/src/js/website_sale_delivery_colissimo.js',
        ],
    },
    'license': 'LGPL-3',
    'auto_install': True,
}
