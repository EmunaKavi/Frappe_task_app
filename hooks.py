app_name = "event_management"
app_title = "Event Management"
app_publisher = "Frappe"
app_description = "Event Management System for Frappe"
app_email = "info@frappe.io"
app_license = "MIT"
app_version = "0.0.1"

# Modules
app_modules = {
    "Event Management": {
        "color": "#1f8ae8",
        "icon": "octicon octicon-calendar",
        "type": "module",
        "label": "Event Management"
    }
}

# Document Events
doc_events = {
    "Event": {
        "validate": "event_management.event_management.doctype.event.event.Event.validate",
        "on_update": "event_management.event_management.doctype.event.event.Event.on_update",
    },
    "Attendee": {
        "validate": "event_management.event_management.doctype.attendee.attendee.Attendee.validate",
        "on_insert": "event_management.event_management.doctype.attendee.attendee.Attendee.on_insert",
        "on_update": "event_management.event_management.doctype.attendee.attendee.Attendee.on_update",
        "before_delete": "event_management.event_management.doctype.attendee.attendee.Attendee.before_delete",
    },
    "Ticket": {
        "validate": "event_management.event_management.doctype.ticket.ticket.Ticket.validate",
        "on_update": "event_management.event_management.doctype.ticket.ticket.Ticket.on_update",
        "on_submit": "event_management.event_management.doctype.ticket.ticket.Ticket.on_submit",
        "before_cancel": "event_management.event_management.doctype.ticket.ticket.Ticket.before_cancel",
    },
    "Ticket Sales": {
        "validate": "event_management.event_management.doctype.ticket_sales.ticket_sales.TicketSales.validate",
        "on_submit": "event_management.event_management.doctype.ticket_sales.ticket_sales.TicketSales.on_submit",
        "before_cancel": "event_management.event_management.doctype.ticket_sales.ticket_sales.TicketSales.before_cancel",
    }
}

# Desk Sidebar
sidebar_items = "Event Management"

# Custom Pages
standard_sidebar_items = [
    "Awesome Bar",
    "Customize Form",
    "Toggle Sidebar",
]
