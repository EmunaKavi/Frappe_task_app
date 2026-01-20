"""
REST API Endpoints for Event Management System
"""

import frappe
from frappe.utils import cint
from event_management.event_management.utils import (
    get_event_summary,
    get_event_attendees,
    export_attendees_csv,
    get_ticket_sales_report,
    get_available_tickets,
    get_event_revenue_by_ticket_type
)


@frappe.whitelist(allow_guest=False)
def list_events():
    """List all events with basic information"""
    events = frappe.get_all(
        "Event",
        fields=["name", "event_title", "event_date", "location", "capacity", "tickets_available"],
        order_by="event_date asc"
    )
    return events


@frappe.whitelist(allow_guest=False)
def get_event(event_name):
    """Get detailed event information"""
    try:
        event = frappe.get_doc("Event", event_name)
        return {
            "name": event.name,
            "event_title": event.event_title,
            "description": event.description,
            "event_date": event.event_date,
            "location": event.location,
            "capacity": event.capacity,
            "tickets_sold": event.tickets_sold,
            "tickets_available": event.tickets_available,
            "summary": get_event_summary(event_name)
        }
    except frappe.DoesNotExistError:
        frappe.throw(f"Event {event_name} does not exist")


@frappe.whitelist(allow_guest=False)
def create_event(event_title, description, event_date, location, capacity):
    """Create a new event"""
    try:
        event = frappe.get_doc({
            "doctype": "Event",
            "event_title": event_title,
            "description": description,
            "event_date": event_date,
            "location": location,
            "capacity": cint(capacity)
        })
        event.insert(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Event {event.name} created successfully",
            "event_id": event.name
        }
    except frappe.ValidationError as e:
        frappe.throw(f"Validation error: {str(e)}")


@frappe.whitelist(allow_guest=False)
def update_event(event_name, **kwargs):
    """Update an existing event"""
    try:
        event = frappe.get_doc("Event", event_name)
        event.update(kwargs)
        event.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Event {event_name} updated successfully"
        }
    except frappe.DoesNotExistError:
        frappe.throw(f"Event {event_name} does not exist")
    except frappe.ValidationError as e:
        frappe.throw(f"Validation error: {str(e)}")


@frappe.whitelist(allow_guest=False)
def delete_event(event_name):
    """Delete an event"""
    try:
        frappe.delete_doc("Event", event_name, ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Event {event_name} deleted successfully"
        }
    except frappe.DoesNotExistError:
        frappe.throw(f"Event {event_name} does not exist")


@frappe.whitelist(allow_guest=False)
def register_attendee(event_name, attendee_name, email, phone=None):
    """Register an attendee for an event"""
    try:
        attendee = frappe.get_doc({
            "doctype": "Attendee",
            "attendee_name": attendee_name,
            "email": email,
            "phone": phone,
            "event": event_name
        })
        attendee.insert(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Attendee {attendee.name} registered successfully",
            "attendee_id": attendee.name
        }
    except frappe.ValidationError as e:
        frappe.throw(f"Validation error: {str(e)}")


@frappe.whitelist(allow_guest=False)
def create_ticket_sale(ticket_name, event_name, quantity):
    """Create a ticket sale"""
    try:
        sale = frappe.get_doc({
            "doctype": "Ticket Sales",
            "ticket": ticket_name,
            "event": event_name,
            "quantity": cint(quantity)
        })
        sale.insert(ignore_permissions=True)
        frappe.db.commit()
        return {
            "status": "success",
            "message": f"Ticket sale {sale.name} created successfully",
            "sale_id": sale.name,
            "total_amount": sale.total_amount
        }
    except frappe.ValidationError as e:
        frappe.throw(f"Validation error: {str(e)}")


@frappe.whitelist(allow_guest=False)
def get_event_statistics(event_name):
    """Get comprehensive statistics for an event"""
    summary = get_event_summary(event_name)
    revenue_breakdown = get_event_revenue_by_ticket_type(event_name)
    
    return {
        "summary": summary,
        "revenue_breakdown": revenue_breakdown,
        "total_records": len(revenue_breakdown)
    }
