# {feature-title} — 介面契約

## 介面清單
<!-- CMP 欄寫進入點元件,B6 用來把 NFR 綁到元件 -->
| ID | Method | Path | Request | Response | 對應 REQ | 綁定 NFR | CMP |
|---|---|---|---|---|---|---|---|
| API-001 | POST | /foo | `{...}` | 200 `{id}` | REQ-001 | NFR-001 | CMP-001 |

## 錯誤碼
| HTTP | Code | 情境 | 對應 AC |
|---|---|---|---|
| 400 | FOO_INVALID | | AC-001-2 |

## 外部依賴與失敗模式
<!-- 每個 external 非空的 CMP 都要有一列,否則 B4 WARN -->
| 外部系統 | 呼叫點 CMP | 逾時 | 重試 | 降級 | 補償 |
|---|---|---|---|---|---|
