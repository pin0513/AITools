# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Client
  participant API
  participant DB
  participant CalendarService
  U->>Client: BookRoom
  Client->>API: BookRoom
  API->>DB: BookRoom
  DB->>CalendarService: BookRoom
  Client-->>U: ok
```

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Client
  participant API
  participant DB
  U->>Client: CheckInBooking
  Client->>API: CheckInBooking
  API->>DB: CheckInBooking
  Client-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as Admin
  participant Client
  participant API
  participant DB
  U->>Client: ListDailyBookings
  Client->>API: ListDailyBookings
  API->>DB: ListDailyBookings
  Client-->>U: ok
```

