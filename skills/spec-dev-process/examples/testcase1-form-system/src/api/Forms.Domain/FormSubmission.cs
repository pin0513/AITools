namespace Forms.Domain;

/// <summary>表單填寫紀錄(issue-b)。</summary>
public sealed class FormSubmission
{
    public Guid Id { get; private set; }
    public Guid FormId { get; private set; }
    public Guid SubmitterId { get; private set; }
    public DateTime SubmittedAt { get; private set; }
    public IReadOnlyDictionary<string, string> Answers { get; private set; } = new Dictionary<string, string>();

    public static FormSubmission Create(Form form, Guid submitterId, IReadOnlyDictionary<string, string> answers)
    {
        if (form.Status != FormStatus.Published) throw new DomainException("FORM_NOT_PUBLISHED");
        foreach (var f in form.Fields)
            if (f.Required && !answers.ContainsKey(f.Key)) throw new DomainException("FIELD_REQUIRED:" + f.Key);
        return new FormSubmission { Id = Guid.NewGuid(), FormId = form.Id, SubmitterId = submitterId, SubmittedAt = DateTime.UtcNow, Answers = answers };
    }
}
