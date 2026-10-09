# 會員點數兌換 — domain model

## Use Case
### UC-001 PointsAccount 點數足夠時 member 可 redeem Reward (REQ-001)
- 主要參與者: member
- 觸發: member redeem Reward
- 前置條件: 餘額足夠
- 後置條件(成功保證): 建立 Redemption 並呼叫 RewardVendor
- 主流程:
  1. member redeem Reward
  2. 建立 Redemption 並呼叫 RewardVendor
- 替代流程: 無
- 例外流程: 回應 422 INSUFFICIENT_POINTS,不扣點

### UC-002 點數 12 個月後 expire (REQ-002)
- 主要參與者: system
- 觸發: 每月排程執行
- 前置條件: 點數於 13 個月前取得
- 後置條件(成功保證): 寫入 expire PointTransaction,餘額減少
- 主流程:
  1. 每月排程執行
  2. 寫入 expire PointTransaction,餘額減少
- 替代流程: 無
- 例外流程: 無

### UC-003 member 可 view PointTransaction (REQ-003)
- 主要參與者: member
- 觸發: member 開啟紀錄
- 前置條件: member 有 PointTransaction
- 後置條件(成功保證): 每筆 PointTransaction 顯示日期、類型、點數
- 主流程:
  1. member 開啟紀錄
  2. 每筆 PointTransaction 顯示日期、類型、點數
- 替代流程: 無
- 例外流程: 無

## 狀態機
### STM-DOM-001 Redemption.Status (REQ-001)
```mermaid
stateDiagram-v2
  [*] --> Pending: RedeemReward
  Pending --> Fulfilled: VendorConfirmed
  Pending --> Failed: VendorRejected
```

## 領域模型
| 類型 | 名稱 | 不變量 |
|---|---|---|
| Aggregate Root | Redemption | Status: Pending → Fulfilled → Failed |
| Entity | PointsAccount | — |
| Entity | Reward | — |
| Entity | PointTransaction | — |

### CLS-001 Redemption (REQ-001)
```mermaid
classDiagram
  class Redemption { +Id +Status }
  PointsAccount --> Redemption : has
  PointsAccount --> Reward : has
  PointsAccount --> PointTransaction : has
```
