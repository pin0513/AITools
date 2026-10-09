# 會議室預約 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | 員工可預約會議室,時段不得重疊 | functional, domain_rich | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 15 分鐘內報到,否則系統釋放會議室 | functional, state_heavy, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | 管理員可查看每日預約單 | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given 時段空閒
When 員工預約會議室
Then 預約單狀態為已預約

# AC-001-2
Given 時段與其他預約單重疊
When 員工預約會議室
Then 回應 409 SLOT_TAKEN

# AC-002-1
Given 預約單狀態為已預約
When 員工在 15 分鐘內報到
Then 預約單狀態為已報到

# AC-002-2
Given 15 分鐘內未報到
When 系統排程執行
Then 預約單狀態為已釋放,行事曆服務已更新

# AC-003-1
Given 今天有預約單
When 管理員開啟每日檢視
Then 依會議室分組顯示

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 同一時段有 100 個並行預約請求時,只有一張預約單成功。 | user | normal load | API-001 | ok | 100 concurrent → 1 success | API-001 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
