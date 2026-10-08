# {feature-title} — 介面契約

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR |
|---|---|---|---|---|---|---|
| API-001 | POST | /members/{id}/avatar | multipart/form-data file | 200 `{url}` | REQ-001 | NFR-001 |

## 錯誤碼
| HTTP | Code | 情境 | 對應 AC |
|---|---|---|---|
| 400 | AVATAR_TOO_LARGE | > 5MB | AC-001-2 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| AzureBlob | CMP-004 | 10s | 3 次,指數退避 | 回 503 | 無(冪等) |
