# SA2 實體 / 關係

## 實體
| 實體 | 英文 | 屬性 | 來源詞 |
|---|---|---|---|
| 訂單 | Order | Id, Status | Order |
| 退款單 | Refund | Id | Refund |

## 關係
| 來源 | 關係 | 目標 | 多重性 |
|---|---|---|---|
| Order | has | Refund | 1..* |

### CLS-SA-001 (REQ-001)
```mermaid
classDiagram
  class Order
  class Refund
  Order --> Refund : has
```
