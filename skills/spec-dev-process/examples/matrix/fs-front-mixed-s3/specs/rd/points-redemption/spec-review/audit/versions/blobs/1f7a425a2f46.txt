# Survey Mapping

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| 點數帳戶 (PointsAccount) | Aggregate | modify | PointsAccount | src/api/Loyalty.Domain/PointsAccount.cs:5 | |
| Balance rule | Rule | existing | PointsAccount.Balance | src/api/Loyalty.Domain/PointsAccount.cs:8 "Balance" | |
| 兌換單 (Redemption) | Entity | new | Redemption | | |
| GetBalance | Query | existing | GetBalanceQueryHandler | src/api/Loyalty.Application/GetBalanceQueryHandler.cs:8 | |
| RedeemReward | Command | new | RedeemReward | | |
| ExpirePoints | Job | new | ExpirePoints | | |
| ListTransactions | Query | new | ListTransactions | | |
| SqlPointsAccountRepository | Adapter | modify | SqlPointsAccountRepository | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs:5 | |
| RewardVendorClient | Adapter | existing | RewardVendorClient | src/api/Loyalty.Infrastructure/RewardVendorClient.cs:5 | |
| PointsController | Api | modify | PointsController | src/api/Loyalty.Api/Controllers/PointsController.cs:8 | |
| RewardsPage | Page | modify | RewardsPage | src/web/src/pages/RewardsPage.tsx:3; src/web/src/pages/RewardsPage.tsx:4 "getBalance(id)" | |
| PointsAccount type | Type | existing | PointsAccount | src/web/src/types/PointsAccount.ts:4 | |
