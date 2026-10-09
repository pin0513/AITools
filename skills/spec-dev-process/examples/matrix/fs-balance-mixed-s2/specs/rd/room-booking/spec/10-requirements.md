# 會議室預約 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | employee 可 book Room, TimeSlot 不得重疊 | functional, domain_rich | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 15 分鐘內 check in,否則 system release Room | functional, state_heavy, integration | PM§3.2 | AC-002-1, AC-002-2 |
| REQ-003 | admin 可 view 每日 Booking | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given TimeSlot 空閒
When employee book Room
Then Booking 狀態為 Booked

# AC-001-2
Given TimeSlot 與其他 Booking 重疊
When employee book Room
Then 回應 409 SLOT_TAKEN

# AC-002-1
Given Booking 狀態為 Booked
When employee 在 15 分鐘內 check in
Then Booking 狀態為 CheckedIn

# AC-002-2
Given 15 分鐘內未 check in
When system 排程執行
Then Booking 狀態為 Released, CalendarService 已更新

# AC-003-1
Given 今天有 Booking
When admin 開啟每日檢視
Then 依 Room 分組顯示

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 同一 TimeSlot 有 100 個並行 book 請求時,只有一張 Booking 成功。 | user | normal load | API-001 | ok | 100 concurrent → 1 success | API-001 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
