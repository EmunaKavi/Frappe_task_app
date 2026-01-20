import frappe
from frappe.model.document import Document
from datetime import datetime


class Event(Document):
    def validate(self):
        """Validate event data"""
        self.validate_event_date()
        self.validate_capacity()
        self.update_ticket_availability()

    def on_update(self):
        """Update ticket availability on update"""
        self.update_ticket_availability()

    def validate_event_date(self):
        """Ensure event date is not in the past"""
        if self.event_date < datetime.now().date():
            frappe.throw("Event date cannot be in the past")

    def validate_capacity(self):
        """Ensure capacity is positive"""
        if self.capacity <= 0:
            frappe.throw("Capacity must be greater than 0")

    def update_ticket_availability(self):
        """Update available tickets based on capacity and sold tickets"""
        self.tickets_sold = frappe.db.count(
            "Attendee",
            filters={"event": self.name}
        )
        self.tickets_available = self.capacity - (self.tickets_sold or 0)
        if self.tickets_available < 0:
            self.tickets_available = 0
