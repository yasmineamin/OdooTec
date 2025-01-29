{
    'name': 'custom_sales',
    'version': '18.0',
    'summary': 'A custom Sales module',
    'description': 'Manages sales operations and extends functionalities.',
    'author': 'Manar',
    'category': 'Sales',
    'depends': ['base', 'sale', 'sale_management'],  # Add 'sale' if extending the Odoo Sales module
    'data': [
        'security/ir.model.access.csv',
        'security/group.xml',
        'views/sale_order_views.xml',
        'views/qc_review_list.xml'
    ],
    'images': ['projects/custom_sales/custom addons/quotation_center/static/quotation_center_icon.png'],
    'installable': True,
    'application': True,
}
