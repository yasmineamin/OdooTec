# -*- coding: utf-8 -*-
{
    'name': 'Ticketing System',
    'version': '1.0',
    'summary': 'Simple Ticketing Module',
    'author': 'Your Name',
    'category': 'Tools',
    'depends': ['base', 'helpdesk', 'mail'],
    'data': [
        'views/ticket_views.xml',
    ],

    'assets': {
        'web.assets_backend': [],
        'web.assets_frontend': [],
    },

    'images': ['Ticketing/custom_addons/Tickets/static/description/icon.png'],  # Path to your icon
    'installable': True,
    'application': True,
}
