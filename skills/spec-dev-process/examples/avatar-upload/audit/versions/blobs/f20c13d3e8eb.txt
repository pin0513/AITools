# 會員上傳大頭貼 — 介面契約

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /members/{id}/avatar | multipart/form-data file | 200 `{url}` | REQ-001 | NFR-001 | CMP-001 |
| API-002 | GET | /members/{id}/avatar-url | — | 200 `{url, expiresAt}` | REQ-003 | NFR-002 | CMP-001 |

## 錯誤碼
| HTTP | Code | 情境 | 對應 AC |
|---|---|---|---|
| 400 | AVATAR_TOO_LARGE | > 5MB | AC-001-2 |
| 400 | AVATAR_NOT_SQUARE | 非正方形或 < 200px | AC-002-1 |
| 503 | STORAGE_UNAVAILABLE | Blob 重試 3 次仍失敗 | AC-001-3 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| AzureBlob | CMP-004 | 10s | 3 次,指數退避 | 回 503,Avatar 不變 | 無(上傳冪等,以 MemberId 為 blob 名) |
