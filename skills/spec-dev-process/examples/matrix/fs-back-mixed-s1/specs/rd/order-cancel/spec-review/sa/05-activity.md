# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["customer cancel Order"] --> B{"Order 狀態為 Placed?"}
  B -->|yes| C["Order 狀態為 Cancelled"]
  B -->|no| D["回應 409 ORDER_SHIPPED,狀態不變"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["system refund"] --> B{"Order 已 cancel 且已付款?"}
  B -->|yes| C["呼叫 PaymentGateway, Order 狀態為 Refunded"]
  B -->|no| D["重試 3 次, Order 維持 Cancelled"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["support agent 開啟紀錄"] --> B{"有 Order 已 cancel?"}
  B -->|yes| C["每列顯示 Order、時間與原因"]
  B -->|no| E["—"]
```

