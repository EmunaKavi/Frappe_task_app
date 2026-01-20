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

<img width="1881" height="888" alt="image" src="https://github.com/user-attachments/assets/3180ead3-ac48-4e06-ba09-9348d1520f2c" />
<img width="1263" height="660" alt="image" src="https://github.com/user-attachments/assets/c1d01945-5dae-4924-acdf-c8340c60e375" />
<img width="1894" height="935" alt="Screenshot 2026-01-20 120410" src="https://github.com/user-attachments/assets/7c94859d-c468-4f7f-a6da-ce1b8b0dd8ea" />
<img width="1894" height="982" alt="Screenshot 2026-01-20 120102" src="https://github.com/user-attachments/assets/f2f288c3-8966-4373-bc30-e84b30620601" />
<img width="1891" height="962" alt="Screenshot 2026-01-20 120119" src="https://github.com/user-attachments/assets/7dce24bf-9f01-4f64-ad74-5066be0743ba" />
<img width="1907" height="984" alt="Screenshot 2026-01-20 120011" src="https://github.com/user-attachments/assets/f6043079-2a72-4de6-8546-0b052779af9b" />
<img width="1900" height="976" alt="Screenshot 2026-01-20 120037" src="https://github.com/user-attachments/assets/c129bb96-4847-40a7-b429-4f087fe15db3" />
<img width="1903" height="983" alt="Screenshot 2026-01-20 115857" src="https://github.com/user-attachments/assets/787111a7-1b25-490d-a233-12259b9a7ced" />
<img width="1084" height="968" alt="Screenshot 2026-01-20 115940" src="https://github.com/user-attachments/assets/390ec3d7-35c7-4ed6-ba83-09acbce999c0" />

