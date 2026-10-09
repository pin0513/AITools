-- issue-a
CREATE TABLE Form (
    Id uniqueidentifier NOT NULL PRIMARY KEY,
    Title nvarchar(200) NOT NULL,
    Status int NOT NULL DEFAULT 0,
    OwnerId uniqueidentifier NOT NULL
);
CREATE TABLE FormField (
    FormId uniqueidentifier NOT NULL REFERENCES Form(Id),
    [Key] nvarchar(50) NOT NULL,
    Label nvarchar(200) NOT NULL,
    Type nvarchar(20) NOT NULL,
    Required bit NOT NULL,
    PRIMARY KEY (FormId, [Key])
);
