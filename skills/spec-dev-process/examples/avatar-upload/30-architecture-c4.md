# 會員上傳大頭貼 — 架構(C4)

## Context(L1)
### C4-L1
```mermaid
C4Context
  Person(member, "會員")
  System(sys, "會員系統")
  System_Ext(blob, "Azure Blob Storage")
  Rel(member, sys, "上傳/瀏覽頭像")
  Rel(sys, blob, "存取圖片", "HTTPS")
```

## Container(L2)
### C4-L2
```mermaid
C4Container
  Container(web, "會員 Web", "React", "裁切在前端")
  Container(api, "Member API", ".NET 8", "")
  ContainerDb(db, "SQL Server", "", "Member")
  System_Ext(blob, "Azure Blob", "")
  Rel(web, api, "HTTPS")
  Rel(api, db, "EF Core")
  Rel(api, blob, "SDK")
```

## Component(L3)
| ID | 名稱 | Layer | Context | depends | external | 技術 |
|---|---|---|---|---|---|---|
| CMP-001 | AvatarController | Api | Member | CMP-002, CMP-006 | | ASP.NET Core |
| CMP-002 | UploadAvatarCommandHandler | Application | Member | CMP-003, CMP-004, CMP-005 | | MediatR |
| CMP-003 | Member (Aggregate) | Domain | Member | CMP-005 | | |
| CMP-004 | BlobAvatarStorage : IAvatarStorage | Infrastructure | Member | | AzureBlob | Azure.Storage.Blobs |
| CMP-005 | ImageSharpValidator | Infrastructure | Member | | | SixLabors.ImageSharp |
| CMP-006 | GetAvatarUrlQueryHandler | Application | Member | CMP-004 | | MediatR |

### C4-L3
```mermaid
C4Component
  Component(c1, "AvatarController", "Api")
  Component(c2, "UploadAvatarCommandHandler", "Application")
  Component(c6, "GetAvatarUrlQueryHandler", "Application")
  Component(c3, "Member", "Domain")
  Component(c4, "BlobAvatarStorage", "Infrastructure", "IAvatarStorage")
  Component(c5, "ImageSharpValidator", "Infrastructure")
  Rel(c1, c2, "Send")
  Rel(c1, c6, "Send")
  Rel(c2, c3, "ReplaceAvatar")
  Rel(c2, c4, "IAvatarStorage")
  Rel(c2, c5, "")
  Rel(c3, c5, "B2 FAIL")
  Rel(c6, c4, "IAvatarStorage")
```

## 追溯(AC → 技術元件)
| AC | CMP | via | 職責 |
|---|---|---|---|
| AC-001-1 | CMP-001 | SEQ-001 | 接收 multipart,回 200 + URL |
| AC-001-1 | CMP-002 | SEQ-001 | 編排:驗證 → 存 Blob → ReplaceAvatar |
| AC-001-1 | CMP-003 | SEQ-001 | ReplaceAvatar,發 AvatarReplaced |
| AC-001-1 | CMP-004 | SEQ-001 | 存 Blob,回 BlobRef |
| AC-001-2 | CMP-001 | SEQ-001 | 格式檢查:大小 > 5MB → 400 |
| AC-001-3 | CMP-004 | SEQ-001 | 逾時重試 3 次後丟 StorageUnavailable |
| AC-001-3 | CMP-002 | SEQ-001 | 捕捉 StorageUnavailable → 503,不呼叫 ReplaceAvatar |
| AC-002-1 | CMP-005 | UC-002 | 後端再驗一次正方形與 ≥ 200px |
| AC-002-1 | CMP-003 | UC-002 | Avatar VO 不變量 |
| AC-003-1 | CMP-006 | UC-003 | 無 Avatar 回預設圖 URL |

## Sequence
### SEQ-001 上傳(UC-001 / REQ-001)
```mermaid
sequenceDiagram
  actor M as 會員
  participant C as AvatarController
  participant H as UploadAvatarCommandHandler
  participant V as ImageSharpValidator
  participant S as IAvatarStorage
  participant A as Member
  M->>C: POST /members/{id}/avatar
  alt size > 5MB
    C-->>M: 400 AVATAR_TOO_LARGE
  else
    C->>H: Send(UploadAvatarCommand)
    H->>V: Validate(stream)
    H->>S: SaveAsync(stream)
    alt Blob 逾時 x3
      S-->>H: StorageUnavailable
      H-->>C: Failure
      C-->>M: 503
    else
      S-->>H: BlobRef
      H->>A: ReplaceAvatar(Avatar)
      A-->>H: AvatarReplaced
      H-->>C: Result(url)
      C-->>M: 200 {url}
    end
  end
```
