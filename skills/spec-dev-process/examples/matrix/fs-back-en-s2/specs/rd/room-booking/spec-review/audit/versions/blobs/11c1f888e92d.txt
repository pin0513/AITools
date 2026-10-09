# Meeting room booking (PM spec)

## 1 Background and Goals
An employee books a meeting room by email today and double booking happens weekly. Goal: self-service book with conflict checks and automatic release.

## 2 Users
employee: wants to book a meeting room. admin: needs the daily view. system: will release no-show booking records.

## 3 Functional Requirements
### 3.1 An employee can book a meeting room without overlapping time slot
An employee can book a meeting room for a time slot. Two booking records on the same meeting room must not overlap. A new booking is booked and is synced to the calendar service.

### 3.2 check in within 15 minutes or the system will release the meeting room
The employee must check in within 15 minutes after the start. Otherwise the system will release the booking, marks it released and updates the calendar service.

### 3.3 An admin can view daily booking records
An admin can view all booking records of a day for every meeting room.

## 4 Non-functional Requirements
With 100 concurrent requests for the same time slot, exactly one booking succeeds.

## 5 Acceptance
- the time slot is free → the employee books the meeting room → a booking is booked
- the time slot overlaps another booking → the employee books the meeting room → the response is 409 SLOT_TAKEN
- a booking is booked → the employee checks in within 15 minutes → the booking is checked-in
- no check in after 15 minutes → the system job runs → the booking is released and the calendar service is updated
- booking records exist today → the admin opens the daily view → rows are grouped by meeting room
