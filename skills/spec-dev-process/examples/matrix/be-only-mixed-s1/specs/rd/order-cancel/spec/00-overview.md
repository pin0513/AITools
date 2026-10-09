# 訂單取消與退款 — overview

## 背景與目標
目前 customer 要 cancel Order 必須打電話給客服。目標: customer 自助 cancel,並由 system 經 PaymentGateway 自動 refund。

## 範圍
純後端

## 名詞表
| 名詞 | 定義 | 來源 |
|---|---|---|
| 訂單 (Order) | Order | PM§3.1 |
| 退款單 (Refund) | Refund | PM§1 |

## 來源對照
| PM 來源 | RD 產物 |
|---|---|
| PM§1 | 00-overview.md |
| PM§3.1 | REQ-001, UC-001 |
| PM§3.2 | REQ-002, UC-002 |
| PM§3.3 | REQ-003, UC-003 |
| PM§4 | NFR-001 |

## 來源
- PM spec: `specs/in-progress/order-cancel/pm-spec.md`
- refs: `specs/in-progress/order-cancel/refs.md`
