import frappe
import unittest
from frappe.tests.utils import FrappeTestCase
from datetime import datetime, timedelta


class TestEvent(FrappeTestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.test_event_data = {
            "doctype": "Event",
            "event_title": "Test Event",
            "description": "Test event description",
            "event_date": (datetime.now() + timedelta(days=30)).date(),
            "location": "Test Location",
            "capacity": 100
        }

    def test_event_creation(self):
        """Test creating a new event"""
        event = frappe.get_doc(self.test_event_data)
        event.insert(ignore_if_duplicate=True)
        self.assertIsNotNone(event.name)
        self.assertEqual(event.event_title, "Test Event")
        self.assertEqual(event.capacity, 100)
        self.assertEqual(event.tickets_available, 100)

    def test_event_past_date_validation(self):
        """Test that event date cannot be in the past"""
        past_event = frappe.get_doc({
            "doctype": "Event",
            "event_title": "Past Event",
            "description": "Past event description",
            "event_date": (datetime.now() - timedelta(days=1)).date(),
            "location": "Test Location",
            "capacity": 50
        })
        with self.assertRaises(frappe.ValidationError):
            past_event.insert()

    def test_event_capacity_validation(self):
        """Test that capacity must be positive"""
        invalid_event = frappe.get_doc({
            "doctype": "Event",
            "event_title": "Invalid Event",
            "description": "Invalid event",
            "event_date": (datetime.now() + timedelta(days=30)).date(),
            "location": "Test Location",
            "capacity": -10
        })
        with self.assertRaises(frappe.ValidationError):
            invalid_event.insert()

    def test_event_unique_title(self):
        """Test that event titles are unique"""
        event1 = frappe.get_doc(self.test_event_data)
        event1.insert(ignore_if_duplicate=True)
        
        duplicate_event = frappe.get_doc(self.test_event_data)
        with self.assertRaises(frappe.DuplicateEntryError):
            duplicate_event.insert()

    def tearDown(self):
        """Clean up test data"""
        frappe.db.delete("Event", filters={"event_title": "Test Event"})
        frappe.db.delete("Event", filters={"event_title": "Invalid Event"})
