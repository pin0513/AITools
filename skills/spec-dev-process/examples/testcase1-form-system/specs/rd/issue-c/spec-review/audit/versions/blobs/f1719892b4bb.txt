# issue-c SA1 斷詞

來源:`specs/in-progress/issue-c/pm-spec.md`(PM§)、`mock/approval.html`(mock)。每個詞記來源,歸類為 實體候選 / 動作候選 / Actor 候選 / 屬性 / 丟棄。

## 名詞
| 詞 | 詞性 | 來源 | 歸類 |
|---|---|---|---|
| 表單 | 名詞 | PM§1 | 實體候選(既有 Form) |
| 填寫紀錄 | 名詞 | PM§3.1 | 實體候選(既有 FormSubmission) |
| 待審核 / 已核准 / 已退回 | 名詞(狀態) | PM§3.1, §3.2, mock data-state | 屬性:FormSubmission.Status |
| 審核紀錄 | 名詞 | PM§3.2, mock #history | 實體候選(新) |
| 理由 | 名詞 | PM§3.2 | 屬性:ReviewRecord.Reason |
| 提醒 | 名詞 | PM§3.4 | 動作候選(系統) |
| 工作天 | 名詞 | PM§3.4 | 屬性:SLA 計算規則 |
| 待審清單 | 名詞 | PM§2 | 查詢候選 |

## 動詞
| 詞 | 詞性 | 來源 | 歸類 |
|---|---|---|---|
| 送出 / 送審 | 動詞 | PM§3.1 | 動作:Submit(既有,語意改變:進入待審核) |
| 核准 | 動詞 | PM§3.2 | 動作:Approve(新) |
| 退回 | 動詞 | PM§3.2 | 動作:Reject(新) |
| 修改 | 動詞 | PM§3.1, §3.3 | 動作:Edit(受狀態限制) |
| 重新送出 | 動詞 | PM§3.3 | 動作:Resubmit(新) |
| 提醒 | 動詞 | PM§3.4 | 動作:Remind(系統,新) |
| 指派 | 動詞 | PM§4 | 動作:Assign reviewer(PM 未展開,列缺口) |

## 角色詞
| 詞 | 詞性 | 來源 | 歸類 |
|---|---|---|---|
| 填寫者 | 角色 | PM§2 | Actor:Submitter(既有 SubmitterId) |
| 審核者 | 角色 | PM§2, §4 | Actor:Reviewer(新) |
| 部門主管 | 角色 | PM§1 | 丟棄:需求來源,非系統 Actor |
| 系統 | 角色 | PM§2, §3.4 | Actor:System(排程) |
