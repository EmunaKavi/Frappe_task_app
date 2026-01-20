import frappe
import unittest
from frappe.tests.utils import FrappeTestCase
from datetime import datetime, timedelta


class TestTicket(FrappeTestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create test event
        self.event = frappe.get_doc({
            "doctype": "Event",
            "event_title": "Test Event for Ticket",
            "description": "Test event",
            "event_date": (datetime.now() + timedelta(days=30)).date(),
            "location": "Test Location",
            "capacity": 100
        })
        self.event.insert(ignore_if_duplicate=True)

        self.test_ticket_data = {
            "doctype": "Ticket",
            "event": self.event.name,
            "ticket_type": "General Admission",
            "price": 50.00,
            "quantity": 100
        }

    def test_ticket_creation(self):
        """Test creating a new ticket"""
        ticket = frappe.get_doc(self.test_ticket_data)
        ticket.insert(ignore_if_duplicate=True)
        self.assertIsNotNone(ticket.name)
        self.assertEqual(ticket.ticket_type, "General Admission")
        self.assertEqual(ticket.price, 50.00)
        self.assertEqual(ticket.quantity, 100)
        self.assertEqual(ticket.available_quantity, 100)

    def test_ticket_price_validation(self):
        """Test that ticket price cannot be negative"""
        invalid_ticket = frappe.get_doc({
            "doctype": "Ticket",
            "event": self.event.name,
            "ticket_type": "Invalid Ticket",
            "price": -10.00,
            "quantity": 50
        })
        with self.assertRaises(frappe.ValidationError):
            invalid_ticket.insert()

    def test_ticket_quantity_validation(self):
        """Test that ticket quantity must be positive"""
        invalid_ticket = frappe.get_doc({
            "doctype": "Ticket",
            "event": self.event.name,
            "ticket_type": "Invalid Ticket",
            "price": 50.00,
            "quantity": 0
        })
        with self.assertRaises(frappe.ValidationError):
            invalid_ticket.insert()

    def test_available_quantity_update(self):
        """Test that available quantity is calculated correctly"""
        ticket = frappe.get_doc(self.test_ticket_data)
        ticket.insert(ignore_if_duplicate=True)
        
        # Create a ticket sale
        ticket_sale = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": ticket.name,
            "event": self.event.name,
            "quantity": 30
        })
        ticket_sale.insert(ignore_if_duplicate=True)
        
        # Reload ticket and verify available quantity
        ticket.reload()
        self.assertEqual(ticket.available_quantity, 70)

    def tearDown(self):
        """Clean up test data"""
        frappe.db.delete("Ticket Sales", filters={"event": self.event.name})
        frappe.db.delete("Ticket", filters={"event": self.event.name})
        frappe.db.delete("Event", filters={"event_title": "Test Event for Ticket"})
