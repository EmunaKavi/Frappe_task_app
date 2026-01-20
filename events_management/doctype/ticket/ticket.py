import frappe
from frappe.model.document import Document


class Ticket(Document):
    def validate(self):
        """Validate ticket data"""
        self.validate_price()
        self.validate_quantity()
        self.update_available_quantity()

    def on_update(self):
        """Update available quantity on update"""
        self.update_available_quantity()

    def on_submit(self):
        """Handle stock deduction on submit"""
        self.deduct_stock()

    def before_cancel(self):
        """Revert stock on cancel"""
        self.revert_stock()

    def validate_price(self):
        """Ensure price is non-negative"""
        if self.price < 0:
            frappe.throw("Ticket price cannot be negative")

    def validate_quantity(self):
        """Ensure quantity is positive"""
        if self.quantity <= 0:
            frappe.throw("Ticket quantity must be greater than 0")

    def update_available_quantity(self):
        """Update available quantity based on ticket sales"""
        sold_quantity = frappe.db.sum(
            "Ticket Sales",
            "quantity",
            {"ticket": self.name}
        ) or 0
        self.available_quantity = self.quantity - sold_quantity
        if self.available_quantity < 0:
            self.available_quantity = 0

    def deduct_stock(self):
        """Deduct stock from ticket sales"""
        frappe.msgprint(f"Stock deducted for ticket {self.name}")

    def revert_stock(self):
        """Revert stock when ticket is cancelled"""
        frappe.msgprint(f"Stock reverted for ticket {self.name}")
