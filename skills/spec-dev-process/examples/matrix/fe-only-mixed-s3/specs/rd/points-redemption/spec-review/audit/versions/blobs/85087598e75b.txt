# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant Web
  participant BackendAPI
  U->>Web: RedeemReward
  Web->>BackendAPI: RedeemReward
  Web-->>U: ok
```

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant BackendAPI
  U->>BackendAPI: ExpirePoints
  BackendAPI-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as Member
  participant Web
  participant BackendAPI
  U->>Web: ListTransactions
  Web->>BackendAPI: ListTransactions
  Web-->>U: ok
```

