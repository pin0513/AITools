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
