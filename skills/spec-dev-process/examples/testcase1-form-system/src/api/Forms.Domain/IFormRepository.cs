namespace Forms.Domain;

public interface IFormRepository
{
    Task<Form?> GetAsync(Guid id, CancellationToken ct);
    Task AddAsync(Form form, CancellationToken ct);
    Task SaveAsync(CancellationToken ct);
}

public interface IFormSubmissionRepository
{
    Task<FormSubmission?> GetAsync(Guid id, CancellationToken ct);
    Task AddAsync(FormSubmission submission, CancellationToken ct);
    Task SaveAsync(CancellationToken ct);
}
