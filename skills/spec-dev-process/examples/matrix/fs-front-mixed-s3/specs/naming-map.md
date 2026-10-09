# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| Balance rule | Balance |  |  |  | Balance |  |  | points-redemption |
| expire | ExpirePoints |  |  | ExpirePointsJob |  |  |  | points-redemption |
| GetBalance | GetBalance |  |  | GetBalanceQueryHandler |  |  |  | points-redemption |
| view | ListTransactions |  | GET /members/{id}/transactions | ListTransactionsQueryHandler |  |  |  | points-redemption |
| 點數交易 | PointTransaction |  |  |  |  |  |  | points-redemption |
| 點數帳戶 | PointsAccount | PointsAccount |  |  | PointsAccount | SqlPointsAccountRepository | PointsAccounts | points-redemption |
| PointsController | PointsController |  | PointsController |  |  |  |  | points-redemption |
| redeem | RedeemReward |  | POST /members/{id}/redemptions | RedeemRewardCommandHandler |  |  |  | points-redemption |
| 兌換單 | Redemption |  |  |  |  |  | Redemption | points-redemption |
| 獎品 | Reward | RewardsPage, rewardsStore |  | RedeemRewardCommandHandler |  | RewardVendorClient |  | points-redemption |
| RewardVendorClient | RewardVendorClient |  |  |  |  | RewardVendorClient |  | points-redemption |
| RewardsPage | RewardsPage | RewardsPage |  |  |  |  |  | points-redemption |
| SqlPointsAccountRepository | SqlPointsAccountRepository |  |  |  |  | SqlPointsAccountRepository |  | points-redemption |
