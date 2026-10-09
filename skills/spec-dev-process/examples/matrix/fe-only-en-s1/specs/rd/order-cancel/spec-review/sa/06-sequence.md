# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Customer
  participant Web
  participant BackendAPI
  U->>Web: CancelOrder
  Web->>BackendAPI: CancelOrder
  Web-->>U: ok
```
