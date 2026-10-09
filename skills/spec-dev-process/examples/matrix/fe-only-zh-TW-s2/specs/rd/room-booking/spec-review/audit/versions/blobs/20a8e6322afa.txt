# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Web
  participant BackendAPI
  U->>Web: BookRoom
  Web->>BackendAPI: BookRoom
  Web-->>U: ok
```

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as Employee
  participant Web
  participant BackendAPI
  U->>Web: CheckInBooking
  Web->>BackendAPI: CheckInBooking
  Web-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as Admin
  participant Web
  participant BackendAPI
  U->>Web: ListDailyBookings
  Web->>BackendAPI: ListDailyBookings
  Web-->>U: ok
```

