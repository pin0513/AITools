# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["member redeem Reward"] --> B{"餘額足夠?"}
  B -->|yes| C["建立 Redemption 並呼叫 RewardVendor"]
  B -->|no| D["回應 422 INSUFFICIENT_POINTS,不扣點"]
```
