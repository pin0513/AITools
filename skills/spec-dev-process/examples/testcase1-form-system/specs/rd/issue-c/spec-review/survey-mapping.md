# issue-c Survey Mapping(模型 ↔ codebase)

候選來源:`survey-candidates.md`(analyze.survey 掃 `src/`);定案規則:existing = 沿用不改;modify = 既有要改;new = 不存在。證據 `path:line` 由 G-SV-evidence 回 codebase 驗證。

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| Form | Aggregate | modify | Forms.Domain.Form | src/api/Forms.Domain/Form.cs:6 | 加 ReviewerIds(審核者指派;PM 未展開,見缺口 #1) |
| FormSubmission | Aggregate | modify | Forms.Domain.FormSubmission | src/api/Forms.Domain/FormSubmission.cs:4 | 加 Status 狀態機、Approve/Reject/Resubmit、ResubmitCount |
| ReviewRecord | Entity | new | Forms.Domain.ReviewRecord | | 屬 FormSubmission aggregate 內的 Entity |
| ReviewReminder | Entity | new | Forms.Domain.ReviewReminder | | 記錄已提醒,避免同日重複 |
| Submit (SubmitFormCommandHandler) | Command | modify | FormsController.Submit / SubmitFormCommandHandler | src/api/Forms.Api/Controllers/FormsController.cs:16; src/api/Forms.Application/Forms/SubmitFormCommandHandler.cs:8 | 送出後 Status=Pending(原本直接生效) |
| Approve | Command | new | ApproveSubmissionCommandHandler | | |
| Reject | Command | new | RejectSubmissionCommandHandler | | 理由 ≥ 10 字 |
| Resubmit | Command | new | ResubmitSubmissionCommandHandler | | |
| ListPending | Query | new | PendingReviewsQueryHandler | | |
| Remind | Job | new | ReviewReminderJob(Hosted Service) | | 每日;逾時 3 工作天 |
| INotifier | Port | existing | Forms.Infrastructure.INotifier / EmailNotifier | src/api/Forms.Infrastructure/EmailNotifier.cs:4 | 退回通知與逾時提醒都走它(guidelines) |
| IFormSubmissionRepository | Port | modify | Forms.Domain.IFormSubmissionRepository | src/api/Forms.Domain/IFormRepository.cs:10 | 加 ListPendingAsync、ListOverdueAsync |
| SqlFormSubmissionRepository | Adapter | modify | Forms.Infrastructure.SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs:14 | 實作新查詢 |
| FormsDbContext | Adapter | modify | Forms.Infrastructure.Persistence.FormsDbContext | src/api/Forms.Infrastructure/Persistence/FormsDbContext.cs:6 | 加 ReviewRecord、ReviewReminder 映射 |
| FormSubmission table | Table | modify | src/database/002_submissions.sql | src/database/002_submissions.sql:2 | 加 Status、ResubmitCount 欄 |
| ReviewRecord table | Table | new | src/database/003_reviews.sql | | 新表,禁止 DELETE(NFR-002) |
| FormFill | Web | modify | src/web/src/pages/FormFill.tsx | src/web/src/pages/FormFill.tsx:2 | Pending 時停用修改;Rejected 顯示理由與重送 |
| ReviewPanel | Web | new | src/web/src/pages/ReviewPanel.tsx | | 待審清單、核准/退回 |
| submitForm | Web | modify | src/web/src/api/client.ts | src/web/src/api/client.ts:4 | 加 approve / reject / resubmit / listPending 呼叫 |
