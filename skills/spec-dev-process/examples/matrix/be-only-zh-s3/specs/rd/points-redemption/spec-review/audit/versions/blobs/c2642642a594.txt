# SA5 Activity Diagram

## Activity Diagram
### ACT-001 (REQ-001)
```mermaid
flowchart TD
  A["會員兌換獎品"] --> B{"餘額足夠?"}
  B -->|yes| C["建立兌換單並呼叫獎品供應商"]
  B -->|no| D["回應 422 INSUFFICIENT_POINTS,不扣點"]
```

### ACT-002 (REQ-002)
```mermaid
flowchart TD
  A["每月排程執行"] --> B{"點數於 13 個月前取得?"}
  B -->|yes| C["寫入到期點數交易,餘額減少"]
  B -->|no| E["—"]
```

### ACT-003 (REQ-003)
```mermaid
flowchart TD
  A["會員開啟紀錄"] --> B{"會員有點數交易?"}
  B -->|yes| C["每筆點數交易顯示日期、類型、點數"]
  B -->|no| E["—"]
```

