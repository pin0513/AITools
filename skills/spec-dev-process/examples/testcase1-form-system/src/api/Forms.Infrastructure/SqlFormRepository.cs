using Forms.Domain;
using Forms.Infrastructure.Persistence;
using Microsoft.EntityFrameworkCore;

namespace Forms.Infrastructure;

public sealed class SqlFormRepository(FormsDbContext db) : IFormRepository
{
    public Task<Form?> GetAsync(Guid id, CancellationToken ct) => db.Forms.Include(f => f.Fields).FirstOrDefaultAsync(f => f.Id == id, ct);
    public Task AddAsync(Form form, CancellationToken ct) => db.Forms.AddAsync(form, ct).AsTask();
    public Task SaveAsync(CancellationToken ct) => db.SaveChangesAsync(ct);
}

public sealed class SqlFormSubmissionRepository(FormsDbContext db) : IFormSubmissionRepository
{
    public Task<FormSubmission?> GetAsync(Guid id, CancellationToken ct) => db.FormSubmissions.FirstOrDefaultAsync(s => s.Id == id, ct);
    public Task AddAsync(FormSubmission submission, CancellationToken ct) => db.FormSubmissions.AddAsync(submission, ct).AsTask();
    public Task SaveAsync(CancellationToken ct) => db.SaveChangesAsync(ct);
}
