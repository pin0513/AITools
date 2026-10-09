-- issue-b
CREATE TABLE FormSubmission (
    Id uniqueidentifier NOT NULL PRIMARY KEY,
    FormId uniqueidentifier NOT NULL REFERENCES Form(Id),
    SubmitterId uniqueidentifier NOT NULL,
    SubmittedAt datetime2 NOT NULL,
    Answers nvarchar(max) NOT NULL
);
CREATE INDEX IX_FormSubmission_FormId ON FormSubmission(FormId);
