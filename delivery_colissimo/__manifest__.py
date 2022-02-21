# -*- coding: utf-8 -*-
{
    'name': "delivery_colissimo",
    'summary': """ Let's choose a Point Relais® as shipping address """,

    'description': """
        This module allow your customer to choose a Point Relais® and use it as shipping address.
        This module doesn't implement the WebService. It is only the integration of the widget.

        Delivery price pre-configured is an example, you need to adapt the pricing's rules.
    """,
    'category': 'Inventory/Delivery',
    'version': '0.1',
    'depends': ['delivery'],
    'data': [
        'data/data.xml',
        'views/views.xml',
        'views/assets.xml',
        'wizard/choose_delivery_carrier_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'delivery_colissimo/static/src/js/colissimo.js',
            'delivery_colissimo/static/src/scss/colissimo.scss',
        ],
    },
    'license': 'LGPL-3',
}
