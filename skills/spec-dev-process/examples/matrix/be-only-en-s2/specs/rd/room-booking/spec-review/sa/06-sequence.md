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
