# {feature-title} — 架構(C4)

## Context(L1)
```mermaid
C4Context
  Person(member, "會員")
  System(sys, "{系統}")
  System_Ext(ext, "{外部系統}")
  Rel(member, sys, "使用")
  Rel(sys, ext, "呼叫", "HTTPS")
```

## Container(L2)
```mermaid
C4Container
  Container(api, "Web API", ".NET", "")
  ContainerDb(db, "SQL Server", "", "")
  ContainerDb(cache, "Redis", "", "")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | AvatarController | Api | Member | CMP-002 | | ASP.NET Core |
| CMP-002 | UploadAvatarCommandHandler | Application | Member | CMP-003, CMP-004 | | MediatR |
| CMP-003 | Avatar (Aggregate) | Domain | Member | | | |
| CMP-004 | IAvatarStorage → BlobAvatarStorage | Infrastructure | Member | | AzureBlob | Azure.Storage.Blobs |

```mermaid
C4Component
  Component(c1, "AvatarController", "Api")
  Component(c2, "UploadAvatarCommandHandler", "Application")
  Component(c3, "Avatar", "Domain")
  Component(c4, "BlobAvatarStorage", "Infrastructure")
  Rel(c1, c2, "Send")
  Rel(c2, c3, "")
  Rel(c2, c4, "IAvatarStorage")
```

## Sequence
### SEQ-001(對應 UC-001)
```mermaid
sequenceDiagram
  actor M as 會員
  participant C as AvatarController
  participant H as UploadAvatarCommandHandler
  participant S as IAvatarStorage
  M->>C: POST /members/{id}/avatar
  C->>H: Send(UploadAvatarCommand)
  H->>S: SaveAsync(stream)
  S-->>H: BlobRef
  H-->>C: Result
  C-->>M: 200 {url}
```
