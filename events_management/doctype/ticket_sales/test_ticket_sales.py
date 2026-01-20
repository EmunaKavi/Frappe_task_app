import frappe
import unittest
from frappe.tests.utils import FrappeTestCase
from datetime import datetime, timedelta


class TestTicketSales(FrappeTestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create test event
        self.event = frappe.get_doc({
            "doctype": "Event",
            "event_title": "Test Event for Sales",
            "description": "Test event",
            "event_date": (datetime.now() + timedelta(days=30)).date(),
            "location": "Test Location",
            "capacity": 100
        })
        self.event.insert(ignore_if_duplicate=True)

        # Create test ticket
        self.ticket = frappe.get_doc({
            "doctype": "Ticket",
            "event": self.event.name,
            "ticket_type": "VIP",
            "price": 100.00,
            "quantity": 50
        })
        self.ticket.insert(ignore_if_duplicate=True)

        self.test_sales_data = {
            "doctype": "Ticket Sales",
            "ticket": self.ticket.name,
            "event": self.event.name,
            "quantity": 10
        }

    def test_ticket_sales_creation(self):
        """Test creating a new ticket sale"""
        sales = frappe.get_doc(self.test_sales_data)
        sales.insert(ignore_if_duplicate=True)
        self.assertIsNotNone(sales.name)
        self.assertEqual(sales.quantity, 10)
        self.assertEqual(sales.total_amount, 1000.00)  # 10 * 100

    def test_ticket_sales_quantity_validation(self):
        """Test that quantity must be positive"""
        invalid_sales = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": self.ticket.name,
            "event": self.event.name,
            "quantity": 0
        })
        with self.assertRaises(frappe.ValidationError):
            invalid_sales.insert()

    def test_ticket_availability_validation(self):
        """Test that sales cannot exceed available quantity"""
        # Create sale with maximum quantity
        sales1 = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": self.ticket.name,
            "event": self.event.name,
            "quantity": 50
        })
        sales1.insert(ignore_if_duplicate=True)

        # Try to exceed available quantity
        sales2 = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": self.ticket.name,
            "event": self.event.name,
            "quantity": 1
        })
        with self.assertRaises(frappe.ValidationError):
            sales2.insert()

    def test_total_amount_calculation(self):
        """Test that total amount is calculated correctly"""
        sales = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": self.ticket.name,
            "event": self.event.name,
            "quantity": 5
        })
        sales.insert(ignore_if_duplicate=True)
        self.assertEqual(sales.total_amount, 500.00)  # 5 * 100

    def tearDown(self):
        """Clean up test data"""
        frappe.db.delete("Ticket Sales", filters={"event": self.event.name})
        frappe.db.delete("Ticket", filters={"event": self.event.name})
        frappe.db.delete("Event", filters={"event_title": "Test Event for Sales"})
