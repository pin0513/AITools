# 會員上傳大頭貼 — 測試設計

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | UploadAvatarCommandHandlerTests | unit | CMP-002 | AC-001-1, AC-001-3 |
| TST-002 | MemberAggregateTests | unit | CMP-003 | AC-001-1, AC-002-1 |
| TST-003 | AvatarControllerTests | integration | CMP-001 | AC-001-1, AC-001-2 |
| TST-004 | BlobAvatarStorageContractTests | contract | CMP-004 | AC-001-3, AC-N02-1 |
| TST-005 | AvatarUploadLoadTest(k6) | e2e | CMP-001 | AC-N01-1 |

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 load test API-001 | P95 < 2s @ 100 VU, 5MB | CI nightly |
| NFR-002 | 以過期 SAS 請求 Blob | 100% 403 | TST-004 |

## 架構測試
| 規則 | 工具 | 斷言 |
|---|---|---|
| B2 | NetArchTest | Types in Member.Domain should not depend on Member.Infrastructure |
