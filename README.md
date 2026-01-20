# Event Management System – Frappe Framework

## Overview
This application is built on the Frappe Framework to manage events, attendees, and ticket sales with stock control and CSV import.

## Features Implemented

### 1. Event Management
- Create, update, delete events  
- Fields:
  - Event Title  
  - Description  
  - Event Date  
  - Location  
  - Capacity  
- Search & filter by:
  - Event Title  
  - Event Date  

### 2. Attendee Management
- Register attendees for events  
- Prevent duplicate attendee registration  
- View attendees mapped to each event  
- Capacity validation before registration

### 3. Ticket Sales & Stock Control
- Track:
  - Tickets sold  
  - Tickets available  
- Auto stock deduction on submit  
- Stock revert on cancel  
- Revenue calculation

### 4. CSV Import
- Import events using Data Import Tool  
- Supported fields:
  - Event Title  
  - Description  
  - Date  
  - Location  
  - Capacity  

---

## Technical Stack
- Framework: Frappe v15  
- Backend: Python  
- Frontend: Frappe Desk UI  
- Database: MariaDB  

---

## DocTypes Created

1. **Event**
   - event_title  
   - description  
   - event_date  
   - location  
   - capacity  
   - tickets_sold  
   - tickets_available  

2. **Attendee**
   - attendee_name  
   - email  
   - phone  
   - event (Link → Event)

3. **Ticket Sales**
   - ticket (Link → Ticket)  
   - event (Link → Event)  
   - quantity  
   - total_amount  

---

## Server Side Logic

### Stock Update on Submit
- Prevent overselling  
- Auto update tickets_sold  
- Calculate tickets_available

### On Cancel
- Revert stock  
- Recalculate availability

---

## Setup Instructions

```bash
cd frappe-bench
bench get-app event_management <repo-url>
bench --site yoursite.local install-app event_management
bench migrate
bench start

https://drive.google.com/drive/folders/1BLknHFphdOnCC3akkhtFkN0vLrDq5aLD?usp=drive_link
