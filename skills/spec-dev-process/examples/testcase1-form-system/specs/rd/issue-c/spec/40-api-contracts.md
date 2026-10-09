# 表單審核流程 — 介面契約

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /forms/{id}/submissions | answers(既有,行為改:Status=Pending) | 200 `{id, status}` | REQ-001 | | CMP-001 |
| API-002 | POST | /submissions/{id}/approve | — | 200 `{status}` | REQ-002 | NFR-001, NFR-003 | CMP-001 |
| API-003 | POST | /submissions/{id}/reject | `{reason}` | 200 `{status}` | REQ-002 | NFR-001, NFR-003 | CMP-001 |
| API-004 | POST | /submissions/{id}/resubmit | `{answers}` | 200 `{status, resubmitCount}` | REQ-003 | | CMP-001 |
| API-005 | GET | /reviews/pending | — | 200 `[{id, formTitle, submittedAt, overdue}]` | REQ-002 | | CMP-001 |

## 錯誤碼
| HTTP | Code | 情境 | 對應 AC |
|---|---|---|---|
| 400 | REASON_TOO_SHORT | 退回理由 < 10 字 | AC-002-2 |
| 403 | NOT_REVIEWER | 操作者不在 Form.ReviewerIds | AC-N03-1 |
| 409 | SUBMISSION_LOCKED | Pending/Approved 時修改或重送 | AC-001-2, AC-003-2 |
| 409 | INVALID_STATE | 非 Pending 時核准/退回 | AC-002-1 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| SMTP | CMP-007 | 5s | 2 次 | 審核操作仍成功,通知失敗記 log(通知非交易一部分) | 逾時提醒:當日不寫 ReviewReminder,隔日再送 |
