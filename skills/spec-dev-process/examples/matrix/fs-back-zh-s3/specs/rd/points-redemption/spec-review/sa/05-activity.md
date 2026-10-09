# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["會員兌換獎品"] --> B{"餘額足夠?"}
  B -->|yes| C["建立兌換單並呼叫獎品供應商"]
  B -->|no| D["回應 422 INSUFFICIENT_POINTS,不扣點"]
```
