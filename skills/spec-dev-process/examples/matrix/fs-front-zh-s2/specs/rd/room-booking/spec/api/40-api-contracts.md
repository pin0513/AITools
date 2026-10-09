# 會議室預約 — API spec

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /rooms/{id}/bookings | json | 200 | REQ-001 | NFR-001 | CMP-007 |
| API-002 | POST | /bookings/{id}/check-in | json | 200 | REQ-002 |  | CMP-007 |
| API-003 | GET | /bookings/daily | json | 200 | REQ-003 |  | CMP-007 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| CalendarService | CMP-013 | 5s | 3 | 503 | retry next run |
