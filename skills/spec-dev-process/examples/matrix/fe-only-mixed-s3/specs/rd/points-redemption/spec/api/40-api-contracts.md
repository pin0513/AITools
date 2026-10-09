# 會員點數兌換 — API spec

## 介面清單
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /members/{id}/redemptions | json | 200 | REQ-001 | NFR-001 | CMP-005 |
| API-002 | GET | /members/{id}/transactions | json | 200 | REQ-003 |  | CMP-005 |

## 外部依賴與失敗模式
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
| BackendAPI | CMP-005 | 5s | 2 | show error | — |
