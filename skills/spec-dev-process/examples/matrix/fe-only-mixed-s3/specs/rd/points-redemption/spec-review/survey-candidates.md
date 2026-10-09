# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| PointsAccount | src/web/src/types/PointsAccount.ts | 4 | `export type PointsAccount = {` |
| PointsAccount | src/web/src/api/pointsApi.ts | 1 | `import type { PointsAccount } from '../types/PointsAccount';` |
| PointsAccount | src/web/src/api/pointsApi.ts | 3 | `export async function getBalance(id: string): Promise<PointsAccount> {` |
| Redemption | (無) | | |
| Reward | (無) | | |
| PointTransaction | (無) | | |
| RedeemReward | (無) | | |
| ExpirePoints | (無) | | |
| ListTransactions | (無) | | |
| 點數帳戶 (PointsAccount) | src/web/src/types/PointsAccount.ts | 4 | `export type PointsAccount = {` |
| 點數帳戶 (PointsAccount) | src/web/src/api/pointsApi.ts | 1 | `import type { PointsAccount } from '../types/PointsAccount';` |
| 點數帳戶 (PointsAccount) | src/web/src/api/pointsApi.ts | 3 | `export async function getBalance(id: string): Promise<PointsAccount> {` |
| Balance rule | src/web/src/types/PointsAccount.ts | 2 | `export type PointsAccountStatus = 'Balance';` |
| 兌換單 (Redemption) | (無) | | |
| GetBalance → GetBalance/getBalance | src/web/src/api/pointsApi.ts | 3 | `export async function getBalance(id: string): Promise<PointsAccount> {` |
| GetBalance → GetBalance/getBalance | src/web/src/pages/RewardsPage.tsx | 1 | `import { getBalance } from '../api/pointsApi';` |
| GetBalance → GetBalance/getBalance | src/web/src/pages/RewardsPage.tsx | 4 | `void getBalance(id);` |
| RewardsPage | src/web/src/pages/RewardsPage.tsx | 3 | `export function RewardsPage({ id }: { id: string }) {` |
