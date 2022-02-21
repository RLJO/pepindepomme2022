# -*- coding: utf-8 -*-
# Part of AppJetty. See LICENSE file for full copyright and licensing details.

{
    'name': 'Data Feed Manager',
    'summary': 'Manage Product Feeds for Worldwide Shopping Market Places Effectively',
    'description': """Data Feed Manager
odoo product feed
advanced data feed
google data feed
google shopping feed
google shopping data feed
google product feed
google shopping feed management
google product feed management
amazon shopping feed
amazon product feed
bing product feed
bing shopping feed
advanced data feed management
google shopping feed extension
yahoo shopping feed
rss feed
google rss feed
""",
    'category': 'Sale',
    'version': '14.0.1.0.0',
    'author': 'AppJetty',
    'license': 'OPL-1',
    'website': 'https://www.appjetty.com/',
    'depends': [
        'website_sale',
    ],
    'external_dependencies': {
        'python': ['jxmlease']
    },
    'data': [
        'security/ir.model.access.csv',
        'data/feed_mail_templates.xml',
        'views/feeds_sequence.xml',
        'views/views.xml',
        'views/feeds_scheduler.xml',
        'views/templates.xml',
    ],
    'images': ['static/description/splash-screen.png'],
    'application': True,
    'price': 99.00,
    'currency': 'EUR',
}
