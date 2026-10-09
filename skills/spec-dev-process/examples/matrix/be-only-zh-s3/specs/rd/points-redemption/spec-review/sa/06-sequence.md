# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant Client
  participant API
  participant DB
  participant RewardVendor
  U->>Client: RedeemReward
  Client->>API: RedeemReward
  API->>DB: RedeemReward
  DB->>RewardVendor: RedeemReward
  Client-->>U: ok
```

### SEQ-SA-002 (REQ-002)
```mermaid
sequenceDiagram
  actor U as System
  participant API
  participant DB
  U->>API: ExpirePoints
  API->>DB: ExpirePoints
  API-->>U: ok
```

### SEQ-SA-003 (REQ-003)
```mermaid
sequenceDiagram
  actor U as Member
  participant Client
  participant API
  participant DB
  U->>Client: ListTransactions
  Client->>API: ListTransactions
  API->>DB: ListTransactions
  Client-->>U: ok
```

