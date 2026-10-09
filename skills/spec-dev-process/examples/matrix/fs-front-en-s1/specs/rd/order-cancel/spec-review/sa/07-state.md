# SA7 State Diagram

## State Diagram
### STM-SA-001 Order.Status (REQ-001, REQ-002)
```mermaid
stateDiagram-v2
  [*] --> Placed: PlaceOrder
  Placed --> Shipped: Ship
  Placed --> Cancelled: CancelOrder
  Cancelled --> Refunded: IssueRefund
```
