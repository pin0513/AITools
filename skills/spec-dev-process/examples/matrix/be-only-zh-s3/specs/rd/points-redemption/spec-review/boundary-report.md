# 會員點數兌換 — 技術邊界核對報告

<!-- 由 spec-dev.py check 產生,不要手改 -->

| 規則 | 目標 | 狀態 | 證據 | 處置 |
|---|---|---|---|---|
| B1 | NFR-001 | PASS | link → CMP-001 |  |
| B1 | REQ-001 | PASS | link → CMP-001, CMP-002, CMP-005, CMP-006, CMP-007 |  |
| B1 | REQ-002 | PASS | link → CMP-003, CMP-005, CMP-006 |  |
| B1 | REQ-003 | PASS | link → CMP-001, CMP-004, CMP-005, CMP-006 |  |
| B2 | CMP-001 | PASS | Api → CMP-002 (Application) |  |
| B2 | CMP-001 | PASS | Api → CMP-004 (Application) |  |
| B2 | CMP-002 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-002 | PASS | Application → CMP-006 經介面 IPointsAccountRepository |  |
| B2 | CMP-002 | PASS | Application → CMP-007 經介面 IRewardVendor |  |
| B2 | CMP-003 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-003 | PASS | Application → CMP-006 經介面 IPointsAccountRepository |  |
| B2 | CMP-004 | PASS | Application → CMP-005 (Domain) |  |
| B2 | CMP-004 | PASS | Application → CMP-006 經介面 IPointsAccountRepository |  |
| B4 | CMP-007 | PASS | RewardVendor 在 Infrastructure 且有失敗模式 |  |
| B5 | PointsAccounts | PASS | owner = Loyalty |  |
| B5 | Redemption | PASS | owner = Loyalty |  |
| B6 | NFR-001 | PASS | 綁定 API-001 |  |
| B7 | AC-001-1 | PASS | → TST-001, TST-002, TST-005, TST-006, TST-007 |  |
| B7 | AC-001-2 | PASS | → TST-001, TST-002, TST-005, TST-006, TST-007 |  |
| B7 | AC-002-1 | PASS | → TST-003, TST-005, TST-006 |  |
| B7 | AC-003-1 | PASS | → TST-001, TST-004, TST-005, TST-006 |  |
| B7 | AC-N01-1 | PASS | → TST-008 |  |
