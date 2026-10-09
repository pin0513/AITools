# 分層命名對照表(跨 spec)

<!-- 由 analyze.glossary 產生,不手改。要修正某格,寫在 specs/naming-overrides.md(同欄位,有值的格子覆蓋這裡)-->

## 分層命名對照

| 名詞 | 符號 | UI | API | Application | Domain | Infrastructure | DB | 來源 spec |
|---|---|---|---|---|---|---|---|---|
| 審核:Pending → Approved,寫 ReviewRecord | Approve |  | POST /submissions/{id}/approve | ApproveSubmissionCommandHandler |  |  |  | issue-c |
| 必填檢查 | Create |  |  |  | Create |  |  | issue-c |
| 退回修改:看理由 → 改答案 | Edit |  | 限 Rejected |  |  |  |  | issue-c |
| 表單 | Form |  |  |  | FormSubmission, Form | SqlFormSubmissionRepository | Form, FormSubmission | issue-b, issue-c |
| 填寫紀錄 | FormSubmission |  |  |  | FormSubmission | SqlFormSubmissionRepository | FormSubmission | issue-b, issue-c |
| FormsDbContext | FormsDbContext |  |  |  |  | FormsDbContext |  | issue-c |
| IFormSubmissionRepository | IFormSubmissionRepository |  |  |  | IFormSubmissionRepository |  |  | issue-c |
| 通知 | INotifier |  |  |  |  | INotifier |  | issue-b, issue-c |
| 看待審清單 | ListPending |  | GET /reviews/pending |  |  |  |  | issue-c |
| 審核:Pending → Rejected,寫 ReviewRecord | Reject |  | POST /submissions/{id}/reject, reason ≥ 10 | RejectSubmissionCommandHandler |  |  |  | issue-c |
| 逾時:Pending > 3 工作天 → INotifier → ReviewReminder | Remind |  | 排程,每日 | ReviewReminderJob |  |  | ReviewReminder | issue-c |
| 重送:Rejected → Pending | Resubmit |  | POST /submissions/{id}/resubmit | ResubmitSubmissionCommandHandler |  |  |  | issue-c |
| 審核紀錄 | ReviewRecord |  |  |  |  |  | ReviewRecord | issue-c |
| 提醒 | ReviewReminder |  |  | ReviewReminderJob |  |  | ReviewReminder | issue-c |
| SqlFormSubmissionRepository | SqlFormSubmissionRepository |  |  |  |  | SqlFormSubmissionRepository |  | issue-c |
| 送審:填答 → 送出 → Pending | Submit |  | POST /forms/{id}/submissions, Submit, SubmitFormCommandHandler | ResubmitSubmissionCommandHandler |  |  |  | issue-c |
