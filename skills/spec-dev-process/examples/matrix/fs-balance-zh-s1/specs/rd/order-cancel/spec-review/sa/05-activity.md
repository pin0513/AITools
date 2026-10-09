# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["顧客取消訂單"] --> B{"訂單狀態為已下單?"}
  B -->|yes| C["訂單狀態為已取消"]
  B -->|no| D["回應 409 ORDER_SHIPPED,狀態不變"]
```
