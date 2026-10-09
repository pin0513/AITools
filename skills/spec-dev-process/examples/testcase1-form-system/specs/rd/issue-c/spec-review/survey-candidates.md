# Survey 候選(由 analyze.survey 產生,不手改;定案寫 survey-mapping.md)

| 模型元素 | 候選檔案 | 行 | 片段 |
|---|---|---|---|
| Form | src/database/002_submissions.sql | 4 | `FormId uniqueidentifier NOT NULL REFERENCES Form(Id),` |
| Form | src/database/001_forms.sql | 2 | `CREATE TABLE Form (` |
| Form | src/database/001_forms.sql | 9 | `FormId uniqueidentifier NOT NULL REFERENCES Form(Id),` |
| Form | src/api/Forms.Infrastructure/SqlFormRepository.cs | 9 | `public Task<Form?> GetAsync(Guid id, CancellationToken ct) => db.Forms.Include(f => f.Fields).FirstO` |
| Form | src/api/Forms.Infrastructure/SqlFormRepository.cs | 10 | `public Task AddAsync(Form form, CancellationToken ct) => db.Forms.AddAsync(form, ct).AsTask();` |
| FormSubmission | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| FormSubmission | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| FormSubmission | src/api/Forms.Infrastructure/SqlFormRepository.cs | 16 | `public Task<FormSubmission?> GetAsync(Guid id, CancellationToken ct) => db.FormSubmissions.FirstOrDe` |
| FormSubmission | src/api/Forms.Infrastructure/SqlFormRepository.cs | 17 | `public Task AddAsync(FormSubmission submission, CancellationToken ct) => db.FormSubmissions.AddAsync` |
| FormSubmission | src/api/Forms.Domain/FormSubmission.cs | 4 | `public sealed class FormSubmission` |
| ReviewRecord | (無) | | |
| ReviewReminder | (無) | | |
| Submit | src/api/Forms.Api/Controllers/FormsController.cs | 16 | `public async Task<IActionResult> Submit(Guid id, [FromBody] SubmitFormBody body, CancellationToken c` |
| Submit | src/web/src/pages/FormFill.tsx | 4 | `return <button onClick={() => submitForm(formId, {})}>Submit</button>;` |
| Edit | (無) | | |
| Resubmit | (無) | | |
| ListPending | (無) | | |
| Approve | (無) | | |
| Reject | (無) | | |
| Remind | (無) | | |
| Form → Form/FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| Form → Form/FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 4 | `FormId uniqueidentifier NOT NULL REFERENCES Form(Id),` |
| Form → Form/FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| Form → Form/FormSubmission/SqlFormSubmissionRepository | src/database/001_forms.sql | 2 | `CREATE TABLE Form (` |
| Form → Form/FormSubmission/SqlFormSubmissionRepository | src/database/001_forms.sql | 9 | `FormId uniqueidentifier NOT NULL REFERENCES Form(Id),` |
| FormSubmission → FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| FormSubmission → FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| FormSubmission → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| FormSubmission → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 16 | `public Task<FormSubmission?> GetAsync(Guid id, CancellationToken ct) => db.FormSubmissions.FirstOrDe` |
| FormSubmission → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 17 | `public Task AddAsync(FormSubmission submission, CancellationToken ct) => db.FormSubmissions.AddAsync` |
| 必填檢查 → Create | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| 必填檢查 → Create | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| 必填檢查 → Create | src/database/001_forms.sql | 2 | `CREATE TABLE Form (` |
| 必填檢查 → Create | src/database/001_forms.sql | 8 | `CREATE TABLE FormField (` |
| 必填檢查 → Create | src/api/Forms.Domain/FormSubmission.cs | 12 | `public static FormSubmission Create(Form form, Guid submitterId, IReadOnlyDictionary<string, string>` |
| 填寫紀錄 → FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| 填寫紀錄 → FormSubmission/SqlFormSubmissionRepository | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| 填寫紀錄 → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| 填寫紀錄 → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 16 | `public Task<FormSubmission?> GetAsync(Guid id, CancellationToken ct) => db.FormSubmissions.FirstOrDe` |
| 填寫紀錄 → FormSubmission/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 17 | `public Task AddAsync(FormSubmission submission, CancellationToken ct) => db.FormSubmissions.AddAsync` |
| ReviewReminder → ReviewReminder/ReviewReminderJob | (無) | | |
| Submit (SubmitFormCommandHandler) → Submit/SubmitFormCommandHandler/ResubmitSubmissionCommandHandler | src/api/Forms.Api/Controllers/FormsController.cs | 16 | `public async Task<IActionResult> Submit(Guid id, [FromBody] SubmitFormBody body, CancellationToken c` |
| Submit (SubmitFormCommandHandler) → Submit/SubmitFormCommandHandler/ResubmitSubmissionCommandHandler | src/api/Forms.Application/Forms/SubmitFormCommandHandler.cs | 8 | `public sealed class SubmitFormCommandHandler(IFormRepository forms, IFormSubmissionRepository submis` |
| Submit (SubmitFormCommandHandler) → Submit/SubmitFormCommandHandler/ResubmitSubmissionCommandHandler | src/web/src/pages/FormFill.tsx | 4 | `return <button onClick={() => submitForm(formId, {})}>Submit</button>;` |
| Approve → Approve/approve/ApproveSubmissionCommandHandler | (無) | | |
| Reject → Reject/reject/RejectSubmissionCommandHandler | (無) | | |
| Resubmit → Resubmit/resubmit/ResubmitSubmissionCommandHandler | (無) | | |
| Remind → Remind/ReviewReminderJob/ReviewReminder | (無) | | |
| INotifier | src/api/Forms.Infrastructure/EmailNotifier.cs | 4 | `public interface INotifier { Task NotifyAsync(Guid userId, string template, object model, Cancellati` |
| INotifier | src/api/Forms.Infrastructure/EmailNotifier.cs | 6 | `public sealed class EmailNotifier : INotifier` |
| IFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| IFormSubmissionRepository | src/api/Forms.Domain/IFormRepository.cs | 10 | `public interface IFormSubmissionRepository` |
| IFormSubmissionRepository | src/api/Forms.Application/Forms/SubmitFormCommandHandler.cs | 8 | `public sealed class SubmitFormCommandHandler(IFormRepository forms, IFormSubmissionRepository submis` |
| SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| FormsDbContext | src/api/Forms.Infrastructure/SqlFormRepository.cs | 7 | `public sealed class SqlFormRepository(FormsDbContext db) : IFormRepository` |
| FormsDbContext | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| FormsDbContext | src/api/Forms.Infrastructure/Persistence/FormsDbContext.cs | 6 | `public sealed class FormsDbContext(DbContextOptions<FormsDbContext> options) : DbContext(options)` |
| FormSubmission table → FormSubmission/table/SqlFormSubmissionRepository | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| FormSubmission table → FormSubmission/table/SqlFormSubmissionRepository | src/database/002_submissions.sql | 9 | `CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);` |
| FormSubmission table → FormSubmission/table/SqlFormSubmissionRepository | src/database/001_forms.sql | 2 | `CREATE TABLE Form (` |
| FormSubmission table → FormSubmission/table/SqlFormSubmissionRepository | src/database/001_forms.sql | 8 | `CREATE TABLE FormField (` |
| FormSubmission table → FormSubmission/table/SqlFormSubmissionRepository | src/api/Forms.Infrastructure/SqlFormRepository.cs | 14 | `public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository` |
| ReviewRecord table | src/database/002_submissions.sql | 2 | `CREATE TABLE FormSubmission (` |
| ReviewRecord table | src/database/001_forms.sql | 2 | `CREATE TABLE Form (` |
| ReviewRecord table | src/database/001_forms.sql | 8 | `CREATE TABLE FormField (` |
| FormFill | src/web/src/pages/FormFill.tsx | 2 | `export function FormFill({ formId }: { formId: string }) {` |
| ReviewPanel | (無) | | |
| submitForm | src/web/src/api/client.ts | 4 | `export async function submitForm(formId: string, answers: Record<string, string>): Promise<{ id: str` |
| submitForm | src/web/src/pages/FormFill.tsx | 1 | `import { submitForm } from '../api/client';` |
| submitForm | src/web/src/pages/FormFill.tsx | 4 | `return <button onClick={() => submitForm(formId, {})}>Submit</button>;` |
