# Survey Mapping

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| 點數帳戶 (PointsAccount) | Aggregate | modify | PointsAccount | src/web/src/types/PointsAccount.ts:4 | |
| Balance rule | Rule | existing | PointsAccount.Balance | src/web/src/types/PointsAccount.ts:2 "Balance" | |
| 兌換單 (Redemption) | Entity | new | Redemption | | |
| GetBalance | Query | existing | getBalance | src/web/src/api/pointsApi.ts:3; src/web/src/api/pointsApi.ts:4 "/members" | |
| RedeemReward | Command | new | RedeemReward | | |
| ExpirePoints | Job | new | ExpirePoints | | |
| ListTransactions | Query | new | ListTransactions | | |
| RewardsPage | Page | modify | RewardsPage | src/web/src/pages/RewardsPage.tsx:3; src/web/src/pages/RewardsPage.tsx:4 "getBalance(id)" | |
