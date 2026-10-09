# 會員上傳大頭貼 — 追溯矩陣

<!-- 由 spec-dev.py check 產生,不要手改 -->

需求 5 · 技術元件 6 · 測試元件 5 · 技術邊界 PASS 20/26 · 未覆蓋需求 1

## 需求 × 技術元件 × 測試元件

| REQ | Api | Application | Domain | Infrastructure | unit | integration | contract | e2e | 狀態 |
|---|---|---|---|---|---|---|---|---|---|
| REQ-001 | CMP-001 | CMP-002 | CMP-003 | CMP-004 | TST-001, TST-002 | TST-003 | TST-004 | · | ⚠ |
| REQ-002 | · | · | CMP-003 | CMP-005 | TST-002 | · | · | · | ⚠ |
| REQ-003 | · | CMP-006 | · | · | · | · | · | · | ✗ |
| NFR-001 | · | · | · | · | · | · | · | TST-005 | ⚠ |
| NFR-002 | · | · | · | CMP-004 | · | · | TST-004 | · | ✓ |

## AC → 技術元件 → 測試

| AC | REQ | CMP(職責) | TST |
|---|---|---|---|
| AC-001-1 | REQ-001 | CMP-001(接收 multipart,回 200 + URL), CMP-002(編排:驗證 → 存 Blob → ReplaceAvatar), CMP-003(ReplaceAvatar,發 AvatarReplaced), CMP-004(存 Blob,回 BlobRef) | TST-001, TST-002, TST-003 |
| AC-001-2 | REQ-001 | CMP-001(格式檢查:大小 > 5MB → 400) | TST-003 |
| AC-001-3 | REQ-001 | CMP-004(逾時重試 3 次後丟 StorageUnavailable), CMP-002(捕捉 StorageUnavailable → 503,不呼叫 ReplaceAvatar) | TST-001, TST-004 |
| AC-002-1 | REQ-002 | CMP-005(後端再驗一次正方形與 ≥ 200px), CMP-003(Avatar VO 不變量) | TST-002 |
| AC-003-1 | REQ-003 | CMP-006(無 Avatar 回預設圖 URL) | ✗ |
| AC-N01-1 | NFR-001 | ✗ | TST-005 |
| AC-N02-1 | NFR-002 | ✗ | TST-004 |

## Gate 問題

| 等級 | 規則 | 訊息 |
|---|---|---|
| WARN | G-M-assumed | REQ-002 S2 DDD.ValueObject 證據=assumed:最小邊長 PM 未定義 |
| WARN | G-M-assumed | NFR-001 S1 QualityScenario 證據=assumed:PM 原文只寫『要快』,2s 為假設 |
| FAIL | G-S3-boundary | CMP-003: 反向依賴:Domain → CMP-005 (Infrastructure) |
| FAIL | G-S3-boundary | AC-003-1: AC-003-1(REQ-003)無測試元件 |
