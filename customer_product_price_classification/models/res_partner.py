from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_class = fields.Selection(
        [('A', 'Class A'), ('B', 'Class B'), ('C', 'Class C')],
        string="Customer Class"
    )
