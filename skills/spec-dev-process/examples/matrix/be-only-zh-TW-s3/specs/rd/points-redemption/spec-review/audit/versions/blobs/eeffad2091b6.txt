# SA3 角色與動作

## 角色與動作
| 角色 | 動作 | 流程 | 對應 REQ |
|---|---|---|---|
| 會員 | RedeemReward(POST /members/{id}/redemptions) | 兌換 | REQ-001 |
| 系統 | ExpirePoints(job) | 到期 | REQ-002 |
| 會員 | ListTransactions(GET /members/{id}/transactions) | 查看 | REQ-003 |
