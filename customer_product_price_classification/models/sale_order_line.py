from odoo import models, fields, api
from datetime import datetime


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    price_class = fields.Selection(
        [('A', 'Price A'), ('B', 'Price B'), ('C', 'Price C')],
        string="Price Class",
        required=True,
        default='A'
    )

    @api.onchange('price_class')
    def _onchange_price_class(self):
        """Update the unit price based on the selected price_class."""
        if self.product_id and self.price_class:
            if self.price_class == 'A':
                self.price_unit = self.product_id.price_a
            elif self.price_class == 'B':
                self.price_unit = self.product_id.price_b
            elif self.price_class == 'C':
                self.price_unit = self.product_id.price_c



    @api.onchange('product_id')
    def _onchange_product_id_set_default_price_class(self):
        """Set a default price_class based on the customer's class."""
        if self.product_id and self.order_id.partner_id:
            customer_class = self.order_id.partner_id.customer_class
            if customer_class == 'A':
                self.price_class = 'A'
                self.price_unit = self.product_id.price_a
            elif customer_class == 'B':
                self.price_class = 'B'
                self.price_unit = self.product_id.price_b
            elif customer_class == 'C':
                self.price_class = 'C'
                self.price_unit = self.product_id.price_c

    def write(self, values):
        """
        Log price, quantity, and price class changes to chatter when any of these fields are updated.
        """
        # Check if price, quantity, or price class is updated
        if 'price_unit' in values or 'product_uom_qty' in values or 'price_class' in values:
            # Get old values for price, quantity, and price class
            old_price = self.price_unit
            old_quantity = self.product_uom_qty
            old_class = self.price_class

            # Get the new values from the `values` dictionary
            new_price = values.get('price_unit', old_price)
            new_quantity = values.get('product_uom_qty', old_quantity)
            new_class = values.get('price_class', old_class)

            # Get customer and product details
            customer = self.order_id.partner_id.name or 'Unknown'
            product = self.product_id.name or 'Unknown'

            # Prepare the log message with details
            log_message = f"""
                   Changes Detected in Order Line:
                   - Product: {product}
                   - Customer: {customer}
                   - Original Price: {old_price}
                   - New Price: {new_price}
                   - Original Quantity: {old_quantity}
                   - New Quantity: {new_quantity}
                   - Original Price Class: {old_class or 'None'}
                   - New Price Class: {new_class or 'None'}
                   - Changed By: {self.env.user.name}
                   - Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
               """
            # Post the log message to the chatter
            self.order_id.message_post(body=log_message, message_type='notification')

        return super(SaleOrderLine, self).write(values)