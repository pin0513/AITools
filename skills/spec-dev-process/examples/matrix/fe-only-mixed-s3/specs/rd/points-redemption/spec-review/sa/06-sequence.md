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
