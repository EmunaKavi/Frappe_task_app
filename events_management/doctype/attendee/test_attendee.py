import frappe
import unittest
from frappe.tests.utils import FrappeTestCase
from datetime import datetime, timedelta


class TestAttendee(FrappeTestCase):
    def setUp(self):
        """Set up test fixtures"""
        # Create test event
        self.event = frappe.get_doc({
            "doctype": "Event",
            "event_title": "Test Event for Attendee",
            "description": "Test event",
            "event_date": (datetime.now() + timedelta(days=30)).date(),
            "location": "Test Location",
            "capacity": 2
        })
        self.event.insert(ignore_if_duplicate=True)

        self.test_attendee_data = {
            "doctype": "Attendee",
            "attendee_name": "John Doe",
            "email": "john@example.com",
            "phone": "+1234567890",
            "event": self.event.name
        }

    def test_attendee_creation(self):
        """Test creating a new attendee"""
        attendee = frappe.get_doc(self.test_attendee_data)
        attendee.insert(ignore_if_duplicate=True)
        self.assertIsNotNone(attendee.name)
        self.assertEqual(attendee.attendee_name, "John Doe")
        self.assertEqual(attendee.event, self.event.name)

    def test_duplicate_attendee_prevention(self):
        """Test that duplicate attendee registration is prevented"""
        attendee1 = frappe.get_doc(self.test_attendee_data)
        attendee1.insert(ignore_if_duplicate=True)

        attendee2 = frappe.get_doc(self.test_attendee_data)
        with self.assertRaises(frappe.ValidationError):
            attendee2.insert()

    def test_capacity_validation(self):
        """Test that event capacity is not exceeded"""
        # Create attendees up to capacity
        for i in range(2):
            attendee = frappe.get_doc({
                "doctype": "Attendee",
                "attendee_name": f"Attendee {i}",
                "email": f"attendee{i}@example.com",
                "phone": f"+123456789{i}",
                "event": self.event.name
            })
            attendee.insert(ignore_if_duplicate=True)

        # Try to exceed capacity
        excess_attendee = frappe.get_doc({
            "doctype": "Attendee",
            "attendee_name": "Excess Attendee",
            "email": "excess@example.com",
            "phone": "+19999999999",
            "event": self.event.name
        })
        with self.assertRaises(frappe.ValidationError):
            excess_attendee.insert()

    def tearDown(self):
        """Clean up test data"""
        frappe.db.delete("Attendee", filters={"event": self.event.name})
        frappe.db.delete("Event", filters={"event_title": "Test Event for Attendee"})
