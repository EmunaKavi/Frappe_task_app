# Event Management System – Frappe Framework

## Overview
This application is built on the Frappe Framework to manage events, attendees, and ticket sales with stock control and comprehensive reporting.

## Features Implemented

### 1. Event Management
- Create, update, delete events  
- Automatic ticket availability tracking
- Real-time stock management
- Fields:
  - Event Title (unique)
  - Description  
  - Event Date  
  - Location  
  - Capacity  
  - Tickets Sold (auto-calculated)
  - Tickets Available (auto-calculated)
- Search & filter by:
  - Event Title  
  - Event Date  
  - Location

### 2. Attendee Management
- Register attendees for events  
- Prevent duplicate attendee registration (same email per event)
- Automatic capacity validation before registration
- View attendees mapped to each event  
- Track attendee contact information
- Automatic event ticket count updates

### 3. Ticket Management
- Create multiple ticket types per event (VIP, General, etc.)
- Set ticket pricing and quantities
- Track available ticket inventory
- Automatic stock updates based on sales
- Revenue calculation per ticket type

### 4. Ticket Sales & Stock Control
- Track ticket sales with automatic calculations
- Quantity validation against available stock
- Auto stock deduction on submit  
- Stock revert on cancel  
- Real-time revenue calculation
- Total amount auto-computed from quantity and price

### 5. Reporting & Analytics
- Event summary with attendee count and revenue
- Ticket sales reports with detailed breakdown
- Revenue by ticket type analysis
- Available tickets overview per event
- Bulk attendee operations

### 6. API Endpoints
- RESTful API for all operations
- Webhook support for integrations
- CSV export capabilities

---

## Technical Stack
- Framework: Frappe v15  
- Backend: Python  
- Frontend: Frappe Desk UI  
- Database: MariaDB  

---

## DocTypes Created

### 1. **Event**
   - event_title (Data, Unique, Required)
   - description (Text Editor)
   - event_date (Date, Required)
   - location (Data, Required)
   - capacity (Integer, Required)
   - tickets_sold (Integer, Read-only)
   - tickets_available (Integer, Read-only)

### 2. **Attendee**
   - attendee_name (Data, Required)
   - email (Email, Required)
   - phone (Phone)
   - event (Link → Event, Required)
   - Unique constraint: One email per event

### 3. **Ticket**
   - event (Link → Event, Required)
   - ticket_type (Data, Required)
   - price (Currency, Required)
   - quantity (Integer, Required)
   - available_quantity (Integer, Read-only)

### 4. **Ticket Sales**
   - ticket (Link → Ticket, Required)
   - event (Link → Event, Required)
   - quantity (Integer, Required)
   - total_amount (Currency, Auto-calculated)

---

## Server Side Logic

### Event Doctype
- **Validation**: Event date cannot be in the past, capacity must be positive
- **On Update**: Automatically calculates tickets_sold from attendee count
- **On Update**: Updates tickets_available = capacity - tickets_sold

### Attendee Doctype
- **Validation**: Prevents duplicate registration (same email per event)
- **Validation**: Ensures event has available capacity before adding
- **On Insert/Update/Delete**: Updates parent event's ticket counts

### Ticket Doctype
- **Validation**: Price must be non-negative, quantity must be positive
- **On Update**: Calculates available_quantity = quantity - sold_quantity
- **On Submit**: Triggers stock deduction
- **Before Cancel**: Reverts stock

### Ticket Sales Doctype
- **Validation**: Quantity must be positive
- **Validation**: Ensures available stock for the ticket
- **On Validate**: Auto-calculates total_amount = quantity × ticket_price
- **On Submit**: Deducts stock from ticket
- **Before Cancel**: Reverts stock to ticket

---

## API Endpoints

### Events
- `GET /api/resource/Event` - List all events
- `POST /api/resource/Event` - Create new event
- `GET /api/resource/Event/{name}` - Get event details
- `PUT /api/resource/Event/{name}` - Update event
- `DELETE /api/resource/Event/{name}` - Delete event

### Custom Endpoints
- `frappe.client.call` method="event_management.event_management.api.list_events"
- `frappe.client.call` method="event_management.event_management.api.get_event_statistics"
- `frappe.client.call` method="event_management.event_management.api.get_event_summary"
- `frappe.client.call` method="event_management.event_management.api.create_ticket_sale"
- `frappe.client.call` method="event_management.event_management.api.register_attendee"

### Utility Functions
- `get_event_summary(event_name)` - Complete event summary with statistics
- `get_event_attendees(event_name)` - List all attendees
- `get_ticket_sales_report(event_name)` - Detailed sales report
- `get_event_revenue_by_ticket_type(event_name)` - Revenue breakdown
- `export_attendees_csv(event_name)` - Export attendees as CSV
- `create_bulk_attendees(event_name, attendees_list)` - Bulk registration

---

## Setup Instructions

```bash
cd frappe-bench
bench get-app event_management <repo-url>
bench --site yoursite.local install-app event_management
bench migrate
bench start

Screenshots of the output:
https://drive.google.com/drive/folders/1BLknHFphdOnCC3akkhtFkN0vLrDq5aLD?usp=drive_link
