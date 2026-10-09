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

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant Web
  participant API
  participant DB
  participant PaymentGateway
  U->>Web: IssueRefund
  Web->>API: IssueRefund
  API->>DB: IssueRefund
  DB->>PaymentGateway: IssueRefund
  Web-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as SupportAgent
  participant Web
  participant API
  participant DB
  U->>Web: ListCancellations
  Web->>API: ListCancellations
  API->>DB: ListCancellations
  Web-->>U: ok
```

