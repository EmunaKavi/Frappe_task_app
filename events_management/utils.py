"""
Utility functions for Event Management System
"""

import frappe
import csv
from io import StringIO
from datetime import datetime


@frappe.whitelist()
def get_event_summary(event_name):
    """Get summary of an event including attendee and revenue info"""
    event = frappe.get_doc("Event", event_name)
    
    attendees = frappe.db.count("Attendee", filters={"event": event_name})
    
    ticket_sales = frappe.db.sql(
        """
        SELECT SUM(quantity) as total_quantity, SUM(total_amount) as total_revenue
        FROM `tabTicket Sales`
        WHERE event = %s
        """,
        (event_name,),
        as_dict=True
    )
    
    return {
        "event_name": event.event_title,
        "event_date": event.event_date,
        "location": event.location,
        "capacity": event.capacity,
        "tickets_sold": event.tickets_sold,
        "tickets_available": event.tickets_available,
        "attendees": attendees,
        "total_tickets_sold": ticket_sales[0].get("total_quantity") if ticket_sales else 0,
        "total_revenue": ticket_sales[0].get("total_revenue") if ticket_sales else 0
    }


@frappe.whitelist()
def get_event_attendees(event_name):
    """Get list of attendees for an event"""
    attendees = frappe.get_all(
        "Attendee",
        filters={"event": event_name},
        fields=["name", "attendee_name", "email", "phone"],
        order_by="creation desc"
    )
    return attendees


@frappe.whitelist()
def export_attendees_csv(event_name):
    """Export attendees for an event as CSV"""
    attendees = get_event_attendees(event_name)
    
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=["Name", "Email", "Phone"])
    writer.writeheader()
    
    for attendee in attendees:
        writer.writerow({
            "Name": attendee.get("attendee_name"),
            "Email": attendee.get("email"),
            "Phone": attendee.get("phone")
        })
    
    return output.getvalue()


@frappe.whitelist()
def get_ticket_sales_report(event_name):
    """Get ticket sales report for an event"""
    ticket_sales = frappe.db.sql(
        """
        SELECT 
            ts.name as sales_id,
            t.ticket_type,
            t.price,
            ts.quantity,
            ts.total_amount,
            ts.creation
        FROM `tabTicket Sales` ts
        JOIN `tabTicket` t ON ts.ticket = t.name
        WHERE ts.event = %s
        ORDER BY ts.creation DESC
        """,
        (event_name,),
        as_dict=True
    )
    return ticket_sales


@frappe.whitelist()
def get_available_tickets(event_name):
    """Get available tickets for an event"""
    tickets = frappe.get_all(
        "Ticket",
        filters={"event": event_name},
        fields=["name", "ticket_type", "price", "quantity", "available_quantity"],
        order_by="creation asc"
    )
    return tickets


@frappe.whitelist()
def create_bulk_attendees(event_name, attendees_list):
    """Create multiple attendees at once"""
    if isinstance(attendees_list, str):
        attendees_list = frappe.parse_json(attendees_list)
    
    created_attendees = []
    errors = []
    
    for attendee_data in attendees_list:
        try:
            attendee = frappe.get_doc({
                "doctype": "Attendee",
                "attendee_name": attendee_data.get("name"),
                "email": attendee_data.get("email"),
                "phone": attendee_data.get("phone"),
                "event": event_name
            })
            attendee.insert(ignore_permissions=True)
            created_attendees.append(attendee.name)
        except frappe.ValidationError as e:
            errors.append({
                "name": attendee_data.get("name"),
                "error": str(e)
            })
    
    return {
        "created": created_attendees,
        "errors": errors,
        "total": len(created_attendees),
        "failed": len(errors)
    }


@frappe.whitelist()
def get_event_revenue_by_ticket_type(event_name):
    """Get revenue breakdown by ticket type"""
    revenue = frappe.db.sql(
        """
        SELECT 
            t.ticket_type,
            t.price,
            SUM(ts.quantity) as tickets_sold,
            SUM(ts.total_amount) as revenue
        FROM `tabTicket Sales` ts
        JOIN `tabTicket` t ON ts.ticket = t.name
        WHERE ts.event = %s
        GROUP BY t.ticket_type, t.price
        """,
        (event_name,),
        as_dict=True
    )
    return revenue
