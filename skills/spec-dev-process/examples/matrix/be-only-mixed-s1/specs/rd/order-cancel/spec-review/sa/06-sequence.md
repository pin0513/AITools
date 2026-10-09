# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant Client
  participant API
  participant DB
  U->>Client: CancelOrder
  Client->>API: CancelOrder
  API->>DB: CancelOrder
  Client-->>U: ok
```
