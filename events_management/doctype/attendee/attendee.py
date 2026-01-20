import frappe
from frappe.model.document import Document


class Attendee(Document):
    def validate(self):
        """Validate attendee data"""
        self.validate_duplicate_registration()
        self.validate_event_capacity()

    def on_insert(self):
        """Update event ticket availability when attendee is added"""
        self.update_event_tickets()

    def on_update(self):
        """Update event ticket availability when attendee is modified"""
        self.update_event_tickets()

    def before_delete(self):
        """Update event ticket availability when attendee is deleted"""
        self.update_event_tickets()

    def validate_duplicate_registration(self):
        """Prevent duplicate attendee registration for the same event"""
        existing = frappe.db.exists(
            "Attendee",
            {
                "event": self.event,
                "email": self.email,
                "name": ("!=", self.name)
            }
        )
        if existing:
            frappe.throw(
                f"Attendee with email {self.email} is already registered for this event"
            )

    def validate_event_capacity(self):
        """Ensure event has available capacity"""
        event = frappe.get_doc("Event", self.event)
        if event.tickets_available <= 0:
            frappe.throw(f"No tickets available for event {self.event}")

    def update_event_tickets(self):
        """Update the event's ticket availability"""
        if self.event:
            event = frappe.get_doc("Event", self.event)
            event.update_ticket_availability()
            event.save(ignore_permissions=True)
