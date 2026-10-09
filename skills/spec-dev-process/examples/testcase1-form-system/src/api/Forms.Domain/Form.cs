namespace Forms.Domain;

public enum FormStatus { Draft = 0, Published = 1 }

/// <summary>表單定義(issue-a)。Aggregate Root。</summary>
public sealed class Form
{
    public Guid Id { get; private set; }
    public string Title { get; private set; } = "";
    public FormStatus Status { get; private set; } = FormStatus.Draft;
    public Guid OwnerId { get; private set; }
    private readonly List<FormField> _fields = new();
    public IReadOnlyList<FormField> Fields => _fields;

    public static Form Create(Guid ownerId, string title)
    {
        if (string.IsNullOrWhiteSpace(title)) throw new DomainException("TITLE_REQUIRED");
        return new Form { Id = Guid.NewGuid(), OwnerId = ownerId, Title = title };
    }

    public void AddField(FormField field) => _fields.Add(field);

    public void Publish()
    {
        if (_fields.Count == 0) throw new DomainException("NO_FIELDS");
        Status = FormStatus.Published;
    }
}

public sealed record FormField(string Key, string Label, string Type, bool Required);
public sealed class DomainException(string code) : Exception(code) { public string Code { get; } = code; }
