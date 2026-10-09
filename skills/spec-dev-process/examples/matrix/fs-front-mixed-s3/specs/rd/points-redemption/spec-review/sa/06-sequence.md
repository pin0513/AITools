# SA6 Sequence Diagram

## Sequence Diagram
### SEQ-SA-001 (REQ-001)
```mermaid
sequenceDiagram
  actor U as Member
  participant Web
  participant API
  participant DB
  participant RewardVendor
  U->>Web: RedeemReward
  Web->>API: RedeemReward
  API->>DB: RedeemReward
  DB->>RewardVendor: RedeemReward
  Web-->>U: ok
```
