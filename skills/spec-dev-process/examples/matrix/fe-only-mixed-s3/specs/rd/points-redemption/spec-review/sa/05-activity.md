# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["member redeem Reward"] --> B{"餘額足夠?"}
  B -->|yes| C["建立 Redemption 並呼叫 RewardVendor"]
  B -->|no| D["回應 422 INSUFFICIENT_POINTS,不扣點"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["每月排程執行"] --> B{"點數於 13 個月前取得?"}
  B -->|yes| C["寫入 expire PointTransaction,餘額減少"]
  B -->|no| E["—"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["member 開啟紀錄"] --> B{"member 有 PointTransaction?"}
  B -->|yes| C["每筆 PointTransaction 顯示日期、類型、點數"]
  B -->|no| E["—"]
```

