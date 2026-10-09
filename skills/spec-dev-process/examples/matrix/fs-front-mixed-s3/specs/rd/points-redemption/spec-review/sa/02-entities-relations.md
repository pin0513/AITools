# SA2 實體 / 關係

## 實體
| 實體 | 英文 | 屬性 | 來源詞 |
|---|---|---|---|
| 點數帳戶 | PointsAccount | Id | PointsAccount |
| 兌換單 | Redemption | Id, Status | Redemption |
| 獎品 | Reward | Id | Reward |
| 點數交易 | PointTransaction | Id | PointTransaction |

## 關係
| 來源 | 關係 | 目標 | 多重性 |
|---|---|---|---|
| PointsAccount | has | Redemption | 1..* |
| PointsAccount | has | Reward | 1..* |
| PointsAccount | has | PointTransaction | 1..* |

### CLS-SA-001 (REQ-001)
```mermaid
classDiagram
  class PointsAccount
  class Redemption
  class Reward
  class PointTransaction
  PointsAccount --> Redemption : has
  PointsAccount --> Reward : has
  PointsAccount --> PointTransaction : has
```
