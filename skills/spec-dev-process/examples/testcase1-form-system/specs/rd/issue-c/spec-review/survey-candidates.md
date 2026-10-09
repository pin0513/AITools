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
