# SA7 State Diagram

## State Diagram
### STM-SA-001 Redemption.Status (REQ-001)
```mermaid
stateDiagram-v2
  [*] --> Pending: RedeemReward
  Pending --> Fulfilled: VendorConfirmed
  Pending --> Failed: VendorRejected
```
