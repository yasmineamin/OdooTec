# models/sale_order.py
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('draft_quotation', 'Draft Quotation'),
        ('quotation_center_review', 'Quotation Center Review'), ('draft',),
    ],
        default='draft_quotation',
        ondelete={'quotation_center_review': 'set default'})

    def action_quotation_center_review(self):
        self.write({'state': 'quotation_center_review'})

        # Get all users in the Quotation Center Review group
        quotation_center_group = self.env.ref('custom_sales.group_quotation_center_review')
        partner_ids = quotation_center_group.users.mapped('partner_id.id')

        # Post a message to all users in the Quotation Center Review group
        self.message_post(
            body="The quotation has been sent for Quotation Center Review.",
            subject="Quotation Review Request",
            message_type="notification",  # This will create a message in the users' inbox
            subtype_xmlid="mail.mt_comment",  # Standard comment subtype
            partner_ids=partner_ids,  # Send the message to the group members
        )

    def action_confirm_after_review(self):
        self.write({'state': 'sale'})

    def action_confirm_to_quotation(self):
        self.write({'state': 'draft'})

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
            'params': {
                'menu_id': self.env.ref('custom_sales.menu_sale_order_quotation_center_review').id,
            }
        }

    is_readonly = fields.Boolean(string="Is Readonly", compute="_compute_is_readonly", store=False)

    def _compute_is_readonly(self):
        for record in self:
            # Check if the state is 'draft' or 'quotation_center_review'
            state_readonly = record.state in ['draft', 'quotation_center_review']
            # Check if the user is in the 'group_quotation_center_review' group
            user_in_group = self.env.user.has_group('custom_sales.group_quotation_center_review')
            # Fields are readonly if:
            # - The state is 'draft' or 'quotation_center_review'.
            # - The user is NOT in the 'group_quotation_center_review' group.
            record.is_readonly = state_readonly and not user_in_group
