from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    price_a = fields.Float(string="Price A")
    price_b = fields.Float(string="Price B")
    price_c = fields.Float(string="Price C")







