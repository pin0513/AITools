# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the customer cancels it"] --> B{"an order is placed?"}
  B -->|yes| C["the order status is cancelled"]
  B -->|no| D["the response is 409 ORDER_SHIPPED and the status is unchanged"]
```
