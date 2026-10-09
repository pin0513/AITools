# 會員上傳大頭貼 — 技術邊界核對報告

<!-- 由 spec-dev.py check 產生,不要手改 -->

| 規則 | 目標 | 狀態 | 證據 | 處置 |
|---|---|---|---|---|
| B2 | CMP-003 | FAIL | 反向依賴:Domain → CMP-005 (Infrastructure) | 在 Domain 定義介面,由 Infrastructure 實作 |
| B7 | AC-003-1 | FAIL | AC-003-1(REQ-003)無測試元件 | 60-test-design.md 補對應 |
| B2 | CMP-002 | WARN | Application 依賴 Infrastructure 具體類別 CMP-005 | 為 ImageSharpValidator 定義介面(名稱欄寫 'Impl : IFoo'),Handler 改依賴介面 |
| B7 | CMP-005 | WARN | 無測試元件 | 新增 ImageSharpValidatorTests |
| B7 | CMP-006 | WARN | 無測試元件 | 新增 GetAvatarUrlQueryHandlerTests |
| B8 | CMP-005 | WARN | SixLabors.ImageSharp 有 Spike 但未結案 | Spike 結案後 out 寫 PASS/採用 |
| B1 | NFR-001 | PASS | link → CMP-001 |  |
| B1 | NFR-002 | PASS | link → CMP-001, CMP-004 |  |
| B1 | REQ-001 | PASS | link → CMP-001, CMP-002, CMP-003, CMP-004 |  |
| B1 | REQ-002 | PASS | link → CMP-003, CMP-005 |  |
| B1 | REQ-003 | PASS | link → CMP-006 |  |
| B2 | CMP-001 | PASS | Api → CMP-002 (Application) |  |
| B2 | CMP-001 | PASS | Api → CMP-006 (Application) |  |
| B2 | CMP-002 | PASS | Application → CMP-003 (Domain) |  |
| B2 | CMP-002 | PASS | Application → CMP-004 經介面 IAvatarStorage |  |
| B2 | CMP-006 | PASS | Application → CMP-004 經介面 IAvatarStorage |  |
| B4 | CMP-004 | PASS | AzureBlob 在 Infrastructure 且有失敗模式 |  |
| B5 | MemberAvatar | PASS | owner = Member |  |
| B6 | NFR-001 | PASS | 綁定 API-001 |  |
| B6 | NFR-002 | PASS | 綁定 API-002, CMP-004 |  |
| B7 | AC-001-1 | PASS | → TST-001, TST-002, TST-003 |  |
| B7 | AC-001-2 | PASS | → TST-003 |  |
| B7 | AC-001-3 | PASS | → TST-001, TST-004 |  |
| B7 | AC-002-1 | PASS | → TST-002 |  |
| B7 | AC-N01-1 | PASS | → TST-005 |  |
| B7 | AC-N02-1 | PASS | → TST-004 |  |
