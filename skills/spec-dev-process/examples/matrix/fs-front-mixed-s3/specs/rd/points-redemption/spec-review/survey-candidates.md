# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| PointsAccount | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 7 | `public Task<PointsAccount?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<PointsAccount` |
| PointsAccount | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 6 | `public sealed record GetBalanceQuery(Guid Id) : IRequest<PointsAccount?>;` |
| PointsAccount | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 8 | `public sealed class GetBalanceQueryHandler(IPointsAccountRepository repo) : IRequestHandler<GetBalan` |
| PointsAccount | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 10 | `public Task<PointsAccount?> Handle(GetBalanceQuery q, CancellationToken ct) => repo.GetAsync(q.Id, c` |
| PointsAccount | src/api/Loyalty.Domain/PointsAccount.cs | 5 | `public sealed class PointsAccount` |
| Redemption | (無) | | |
| Reward | (無) | | |
| PointTransaction | (無) | | |
| RedeemReward | (無) | | |
| ExpirePoints | (無) | | |
| ListTransactions | (無) | | |
| 點數帳戶 (PointsAccount) → PointsAccount/SqlPointsAccountRepository/PointsAccounts | src/database/001_pointsaccounts.sql | 2 | `CREATE TABLE PointsAccounts (` |
| 點數帳戶 (PointsAccount) → PointsAccount/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 5 | `public sealed class SqlPointsAccountRepository : IPointsAccountRepository` |
| 點數帳戶 (PointsAccount) → PointsAccount/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 7 | `public Task<PointsAccount?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<PointsAccount` |
| 點數帳戶 (PointsAccount) → PointsAccount/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 6 | `public sealed record GetBalanceQuery(Guid Id) : IRequest<PointsAccount?>;` |
| 點數帳戶 (PointsAccount) → PointsAccount/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 8 | `public sealed class GetBalanceQueryHandler(IPointsAccountRepository repo) : IRequestHandler<GetBalan` |
| Balance rule | src/database/001_pointsaccounts.sql | 4 | `Balance nvarchar(50) NOT NULL` |
| Balance rule | src/api/Loyalty.Domain/PointsAccount.cs | 8 | `public int Balance { get; private set; }` |
| Balance rule | src/web/src/types/PointsAccount.ts | 2 | `export type PointsAccountStatus = 'Balance';` |
| 兌換單 (Redemption) | (無) | | |
| GetBalance → GetBalance/GetBalanceQueryHandler | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 8 | `public sealed class GetBalanceQueryHandler(IPointsAccountRepository repo) : IRequestHandler<GetBalan` |
| GetBalance → GetBalance/GetBalanceQueryHandler | src/api/Loyalty.Api/Controllers/PointsController.cs | 11 | `public async Task<IActionResult> GetBalance(Guid id, CancellationToken ct) => Ok(await sender.Send(n` |
| GetBalance → GetBalance/GetBalanceQueryHandler | src/web/src/api/pointsApi.ts | 3 | `export async function getBalance(id: string): Promise<PointsAccount> {` |
| GetBalance → GetBalance/GetBalanceQueryHandler | src/web/src/pages/RewardsPage.tsx | 1 | `import { getBalance } from '../api/pointsApi';` |
| GetBalance → GetBalance/GetBalanceQueryHandler | src/web/src/pages/RewardsPage.tsx | 4 | `void getBalance(id);` |
| RedeemReward → RedeemReward/RedeemRewardCommandHandler | (無) | | |
| ExpirePoints → ExpirePoints/ExpirePointsJob | (無) | | |
| ListTransactions → ListTransactions/ListTransactionsQueryHandler | (無) | | |
| SqlPointsAccountRepository | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 5 | `public sealed class SqlPointsAccountRepository : IPointsAccountRepository` |
| RewardVendorClient | src/api/Loyalty.Infrastructure/RewardVendorClient.cs | 5 | `public sealed class RewardVendorClient : IRewardVendor` |
| PointsController | src/api/Loyalty.Api/Controllers/PointsController.cs | 8 | `public sealed class PointsController(ISender sender) : ControllerBase` |
| RewardsPage | src/web/src/pages/RewardsPage.tsx | 3 | `export function RewardsPage({ id }: { id: string }) {` |
| PointsAccount type → PointsAccount/type/SqlPointsAccountRepository/PointsAccounts | src/database/001_pointsaccounts.sql | 2 | `CREATE TABLE PointsAccounts (` |
| PointsAccount type → PointsAccount/type/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 5 | `public sealed class SqlPointsAccountRepository : IPointsAccountRepository` |
| PointsAccount type → PointsAccount/type/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Infrastructure/SqlPointsAccountRepository.cs | 7 | `public Task<PointsAccount?> GetAsync(Guid id, CancellationToken ct) => Task.FromResult<PointsAccount` |
| PointsAccount type → PointsAccount/type/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 6 | `public sealed record GetBalanceQuery(Guid Id) : IRequest<PointsAccount?>;` |
| PointsAccount type → PointsAccount/type/SqlPointsAccountRepository/PointsAccounts | src/api/Loyalty.Application/GetBalanceQueryHandler.cs | 8 | `public sealed class GetBalanceQueryHandler(IPointsAccountRepository repo) : IRequestHandler<GetBalan` |
