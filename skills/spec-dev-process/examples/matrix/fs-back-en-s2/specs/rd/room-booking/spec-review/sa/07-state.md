# SA7 State Diagram

## State Diagram
### STM-SA-001 Booking.Status (REQ-001, REQ-002)
```mermaid
stateDiagram-v2
  [*] --> Booked: BookRoom
  Booked --> CheckedIn: CheckInBooking
  Booked --> Released: ReleaseNoShow
```
