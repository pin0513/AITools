# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant Web
  participant API
  participant DB
  U->>Web: CancelOrder
  Web->>API: CancelOrder
  API->>DB: CancelOrder
  Web-->>U: ok
```
