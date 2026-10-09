using Forms.Domain;
using Microsoft.EntityFrameworkCore;

namespace Forms.Infrastructure.Persistence;

public sealed class FormsDbContext(DbContextOptions<FormsDbContext> options) : DbContext(options)
{
    public DbSet<Form> Forms => Set<Form>();
    public DbSet<FormSubmission> FormSubmissions => Set<FormSubmission>();

    protected override void OnModelCreating(ModelBuilder b)
    {
        b.Entity<Form>().ToTable("Form").HasKey(x => x.Id);
        b.Entity<Form>().OwnsMany(x => x.Fields, f => f.ToTable("FormField"));
        b.Entity<FormSubmission>().ToTable("FormSubmission").HasKey(x => x.Id);
    }
}
