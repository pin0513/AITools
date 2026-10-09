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

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant Client
  participant API
  participant DB
  participant PaymentGateway
  U->>Client: IssueRefund
  Client->>API: IssueRefund
  API->>DB: IssueRefund
  DB->>PaymentGateway: IssueRefund
  Client-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as SupportAgent
  participant Client
  participant API
  participant DB
  U->>Client: ListCancellations
  Client->>API: ListCancellations
  API->>DB: ListCancellations
  Client-->>U: ok
```

