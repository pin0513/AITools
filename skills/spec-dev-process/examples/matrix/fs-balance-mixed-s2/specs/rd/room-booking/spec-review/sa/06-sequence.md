# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Web
  participant API
  participant DB
  participant CalendarService
  U->>Web: BookRoom
  Web->>API: BookRoom
  API->>DB: BookRoom
  DB->>CalendarService: BookRoom
  Web-->>U: ok
```

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Web
  participant API
  participant DB
  U->>Web: CheckInBooking
  Web->>API: CheckInBooking
  API->>DB: CheckInBooking
  Web-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as Admin
  participant Web
  participant API
  participant DB
  U->>Web: ListDailyBookings
  Web->>API: ListDailyBookings
  API->>DB: ListDailyBookings
  Web-->>U: ok
```

