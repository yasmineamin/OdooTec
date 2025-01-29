{
    'name': 'Customer & Product Price Classification',
    'version': '1.0',
    'category': 'Sales',
    'summary': 'Adds customer classification and product price classification.',
    'author': 'Your Name',
    'depends': ['base','sale_management'],
    'data': [
        #'security/security.xml',
        #'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
}
