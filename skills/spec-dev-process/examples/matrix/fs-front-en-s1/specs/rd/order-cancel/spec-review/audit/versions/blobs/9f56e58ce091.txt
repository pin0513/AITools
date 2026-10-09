# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["the customer cancels it"] --> B{"an order is placed?"}
  B -->|yes| C["the order status is cancelled"]
  B -->|no| D["the response is 409 ORDER_SHIPPED and the status is unchanged"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["the system issues the refund"] --> B{"an order is cancelled and paid?"}
  B -->|yes| C["the payment gateway is called and the order is refunded"]
  B -->|no| D["it retries 3 times and the order stays cancelled"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["the support agent opens the history"] --> B{"order records were cancelled?"}
  B -->|yes| C["each row shows the order, time and reason"]
  B -->|no| E["—"]
```

