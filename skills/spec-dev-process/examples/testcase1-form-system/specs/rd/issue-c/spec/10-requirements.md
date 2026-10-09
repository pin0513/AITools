# 表單審核流程 — 需求

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | 送出後填寫紀錄進入 Pending,期間填寫者不可修改 | functional, state_heavy | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 審核者核准或退回;退回理由 ≥ 10 字;留下審核紀錄 | functional, domain_rich | PM§3.2 | AC-002-1, AC-002-2, AC-002-3 |
| REQ-003 | 被退回可修改後重送,再入 Pending;已核准不可改 | functional, state_heavy | PM§3.3 | AC-003-1, AC-003-2 |
| REQ-004 | Pending 超過 3 工作天,每日提醒審核者直到處理 | functional, integration | PM§3.4 | AC-004-1, AC-004-2 |

## 驗收條件
```gherkin
# AC-001-1 送出後待審核
Given 已發布表單,填寫者填妥必填欄位
When 送出
Then 回 200,紀錄狀態 = Pending,個人頁顯示「待審核」

# AC-001-2 待審核不可修改
Given 狀態 = Pending 的紀錄
When 填寫者嘗試修改答案
Then 回 409 SUBMISSION_LOCKED,答案不變

# AC-002-1 核准
Given 狀態 = Pending,操作者是該表單指派審核者
When 核准
Then 狀態 = Approved,新增 ReviewRecord(審核者、時間、Approved)

# AC-002-2 退回理由不足
Given 狀態 = Pending
When 退回且理由 < 10 字
Then 回 400 REASON_TOO_SHORT,狀態不變,無 ReviewRecord

# AC-002-3 退回
Given 狀態 = Pending,理由 ≥ 10 字
When 退回
Then 狀態 = Rejected,新增 ReviewRecord(含理由),通知填寫者

# AC-003-1 重送
Given 狀態 = Rejected,填寫者修改答案
When 重新送出
Then 狀態 = Pending,ResubmitCount + 1

# AC-003-2 已核准不可改
Given 狀態 = Approved
When 填寫者嘗試修改或重送
Then 回 409 SUBMISSION_LOCKED

# AC-004-1 逾時提醒
Given 狀態 = Pending 已超過 3 個工作天,今日尚未提醒
When 每日排程執行
Then 對每位指派審核者發出提醒,寫入 ReviewReminder

# AC-004-2 同日不重複
Given 今日已提醒
When 排程再次執行
Then 不再發出提醒
```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 核准/退回操作 | 審核者 | 正常負載 50 VU | API-002, API-003 | 完成並回應 | P95 < 1s | API-002, API-003 | AC-N01-1 |
| NFR-002 | 嘗試刪除或修改審核紀錄 | 任何人 | 任何 | ReviewRecord | 拒絕 | 無 DELETE/UPDATE 路徑;DB 層禁止 | CMP-005, CMP-006 | AC-N02-1 |
| NFR-003 | 非指派審核者呼叫核准/退回 | 任何登入者 | 任何 | API-002, API-003 | 403 | 100% 拒絕 | CMP-002, CMP-003 | AC-N03-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
| 1 | 審核者如何指派(每表單?每部門?) | REQ-002, NFR-003 | Form.ReviewerIds 由設定檔載入,不做 UI |
| 2 | 「要快」沒有數字 | NFR-001 | P95 < 1s @ 50 VU |
| 3 | 工作天是否含國定假日 | REQ-004 | 只排除週六日 |
| 4 | 退回通知填寫者 PM 未明寫(mock 有歷史列) | REQ-002 | 退回時經 INotifier 通知填寫者 |
