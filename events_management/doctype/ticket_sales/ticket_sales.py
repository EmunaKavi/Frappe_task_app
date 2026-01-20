import frappe
from frappe.model.document import Document


class TicketSales(Document):
    def validate(self):
        """Validate ticket sales data"""
        self.validate_quantity()
        self.validate_ticket_availability()
        self.calculate_total_amount()

    def on_submit(self):
        """Handle stock deduction on submit"""
        self.deduct_stock()

    def before_cancel(self):
        """Revert stock on cancel"""
        self.revert_stock()

    def validate_quantity(self):
        """Ensure quantity is positive"""
        if self.quantity <= 0:
            frappe.throw("Ticket quantity must be greater than 0")

    def validate_ticket_availability(self):
        """Ensure ticket has available quantity"""
        ticket = frappe.get_doc("Ticket", self.ticket)
        if ticket.available_quantity < self.quantity:
            frappe.throw(
                f"Only {ticket.available_quantity} tickets available for {self.ticket}"
            )

    def calculate_total_amount(self):
        """Calculate total amount based on ticket price and quantity"""
        ticket = frappe.get_doc("Ticket", self.ticket)
        self.total_amount = ticket.price * self.quantity

    def deduct_stock(self):
        """Deduct stock from ticket availability"""
        ticket = frappe.get_doc("Ticket", self.ticket)
        ticket.update_available_quantity()
        ticket.save(ignore_permissions=True)

    def revert_stock(self):
        """Revert stock when ticket sales is cancelled"""
        ticket = frappe.get_doc("Ticket", self.ticket)
        ticket.update_available_quantity()
        ticket.save(ignore_permissions=True)
