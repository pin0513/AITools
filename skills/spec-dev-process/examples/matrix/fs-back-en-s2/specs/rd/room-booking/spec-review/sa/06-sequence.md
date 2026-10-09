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
