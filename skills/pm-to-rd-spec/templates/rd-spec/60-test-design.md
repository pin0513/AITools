# {feature-title} — 測試設計

## 測試元件清單
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | UploadAvatarCommandHandlerTests | unit | CMP-002 | AC-001-1, AC-001-2 |
| TST-002 | AvatarControllerTests | integration | CMP-001 | AC-001-1 |
| TST-003 | BlobAvatarStorageContractTests | contract | CMP-004 | AC-001-3 |

## AC 對應
| AC | TST | 覆蓋狀態 |
|---|---|---|

## Fitness Function
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 load test API-001 | P95 < 500ms @ 100 VU | CI nightly |
