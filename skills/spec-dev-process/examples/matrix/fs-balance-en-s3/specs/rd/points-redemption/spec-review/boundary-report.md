# Loyalty points redemption — 技術邊界核對報告

<!-- 由 spec-dev.py check 產生,不要手改 -->

| 規則 | 目標 | 狀態 | 證據 | 處置 |
|---|---|---|---|---|
| B1 | NFR-001 | PASS | link → CMP-006 |  |
| B1 | REQ-001 | PASS | link → CMP-001, CMP-002, CMP-004, CMP-005, CMP-006, CMP-007, CMP-010, CMP-011, CMP-012 |  |
| B1 | REQ-002 | PASS | link → CMP-004, CMP-005, CMP-008, CMP-010, CMP-011 |  |
| B1 | REQ-003 | PASS | link → CMP-001, CMP-003, CMP-004, CMP-005, CMP-006, CMP-009, CMP-010, CMP-011 |  |
| B2 | CMP-001 | PASS | Page → CMP-002 (Component) |  |
| B2 | CMP-001 | PASS | Page → CMP-003 (Component) |  |
| B2 | CMP-001 | PASS | Page → CMP-004 (Store) |  |
| B2 | CMP-002 | PASS | Component → CMP-004 (Store) |  |
| B2 | CMP-003 | PASS | Component → CMP-004 (Store) |  |
| B2 | CMP-004 | PASS | Store → CMP-005 (ApiClient) |  |
| B2 | CMP-005 | PASS | ApiClient → CMP-006 (Api) |  |
| B2 | CMP-006 | PASS | Api → CMP-007 (Application) |  |
| B2 | CMP-006 | PASS | Api → CMP-009 (Application) |  |
| B2 | CMP-007 | PASS | Application → CMP-010 (Domain) |  |
| B2 | CMP-007 | PASS | Application → CMP-011 經介面 IPointsAccountRepository |  |
| B2 | CMP-007 | PASS | Application → CMP-012 經介面 IRewardVendor |  |
| B2 | CMP-008 | PASS | Application → CMP-010 (Domain) |  |
| B2 | CMP-008 | PASS | Application → CMP-011 經介面 IPointsAccountRepository |  |
| B2 | CMP-009 | PASS | Application → CMP-010 (Domain) |  |
| B2 | CMP-009 | PASS | Application → CMP-011 經介面 IPointsAccountRepository |  |
| B4 | CMP-012 | PASS | RewardVendor 在 Infrastructure 且有失敗模式 |  |
| B5 | PointsAccounts | PASS | owner = Loyalty |  |
| B5 | Redemption | PASS | owner = Loyalty |  |
| B6 | NFR-001 | PASS | 綁定 API-001 |  |
| B7 | AC-001-1 | PASS | → TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011, TST-012 |  |
| B7 | AC-001-2 | PASS | → TST-001, TST-002, TST-004, TST-005, TST-006, TST-007, TST-010, TST-011, TST-012 |  |
| B7 | AC-002-1 | PASS | → TST-004, TST-005, TST-008, TST-010, TST-011 |  |
| B7 | AC-003-1 | PASS | → TST-001, TST-003, TST-004, TST-005, TST-006, TST-009, TST-010, TST-011 |  |
| B7 | AC-N01-1 | PASS | → TST-013 |  |
