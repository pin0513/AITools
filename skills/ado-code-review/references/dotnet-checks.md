# .NET/C# 專家審查規則

完整的 .NET/C# 程式碼審查規則，用於 ado-code-review skill。

---

## 命名規範

### PascalCase 使用場景

```csharp
// Classes, Methods, Properties, Public Fields
public class UserService { }
public void ProcessOrder() { }
public string FirstName { get; set; }
public const int MaxRetries = 3;
```

### camelCase 使用場景

```csharp
// Private fields: _camelCase
private readonly ILogger _logger;
private int _counter;

// Local variables, parameters
public void Process(string userName)
{
    var result = Calculate(userName);
}
```

### 介面命名

```csharp
// 必須以 I 開頭
public interface IUserService { }
public interface IRepository<T> { }
```

### Async 方法命名

```csharp
// 必須以 Async 結尾
public async Task<User> GetUserAsync(int id) { }
public async Task ProcessOrderAsync(Order order) { }
```

---

## 程式碼結構

### 方法長度限制

```
❌ VIOLATION: 方法超過 50 行
   建議：拆分為多個私有方法，每個方法做一件事
```

### 檔案長度限制

```
❌ VIOLATION: 檔案超過 800 行
   建議：拆分為多個類別，使用 partial class 或提取服務
```

### 巢狀深度限制

```csharp
// ❌ BAD: 巢狀深度 > 4 層
if (user != null)
{
    if (user.IsActive)
    {
        if (user.HasPermission)
        {
            if (user.Roles.Any())
            {
                // 太深了
            }
        }
    }
}

// ✅ GOOD: 使用早期返回
if (user is null) return;
if (!user.IsActive) return;
if (!user.HasPermission) return;
if (!user.Roles.Any()) return;

// 主要邏輯
```

### 類別成員順序

```csharp
public class UserService : IUserService
{
    // 1. Constants
    private const int MaxAttempts = 3;

    // 2. Static fields
    private static readonly object _lock = new();

    // 3. Instance fields
    private readonly ILogger<UserService> _logger;
    private readonly IUserRepository _repository;

    // 4. Constructors
    public UserService(ILogger<UserService> logger) { }

    // 5. Properties
    public int RetryCount { get; private set; }

    // 6. Public methods
    public async Task<User> GetByIdAsync(int id) { }

    // 7. Private methods
    private void LogAttempt(int attempt) { }
}
```

---

## Async/Await 規則

### 必須使用 async/await

```csharp
// ❌ BAD: 阻塞式呼叫
var user = GetUserAsync(1).Result;
var order = ProcessOrderAsync().Wait();

// ✅ GOOD: 非阻塞式
var user = await GetUserAsync(1);
var order = await ProcessOrderAsync();
```

### ConfigureAwait(false) 在 Library Code

```csharp
// ✅ Library code 應使用 ConfigureAwait(false)
public async Task<User> GetUserAsync(int id)
{
    return await _repository.GetByIdAsync(id).ConfigureAwait(false);
}
```

### CancellationToken 傳遞

```csharp
// ❌ BAD: 缺少 CancellationToken
public async Task ProcessAsync()
{
    await _httpClient.GetAsync(url);
}

// ✅ GOOD: 傳遞 CancellationToken
public async Task ProcessAsync(CancellationToken cancellationToken = default)
{
    await _httpClient.GetAsync(url, cancellationToken);
}
```

### 避免 Task.Run 在 ASP.NET Core

```csharp
// ❌ BAD: ASP.NET Core 中使用 Task.Run
public async Task<IActionResult> Get()
{
    var result = await Task.Run(() => HeavyComputation());
    return Ok(result);
}

// ✅ GOOD: 直接使用 async
public async Task<IActionResult> Get()
{
    var result = await HeavyComputationAsync();
    return Ok(result);
}
```

---

## 錯誤處理

### 使用特定例外類型

```csharp
// ❌ BAD: 使用通用 Exception
throw new Exception("User not found");

// ✅ GOOD: 使用特定例外
throw new ArgumentNullException(nameof(userId));
throw new InvalidOperationException("User not found");
throw new NotFoundException($"User {userId} not found");
```

### 捕捉特定例外

```csharp
// ❌ BAD: 捕捉通用 Exception
try
{
    await ProcessAsync();
}
catch (Exception ex)
{
    _logger.LogError(ex, "Error");
}

// ✅ GOOD: 捕捉特定例外
try
{
    await ProcessAsync();
}
catch (HttpRequestException ex)
{
    _logger.LogError(ex, "HTTP request failed");
    throw;
}
catch (OperationCanceledException)
{
    _logger.LogWarning("Operation cancelled");
    throw;
}
```

---

## Entity Framework Core

### 避免 N+1 查詢

```csharp
// ❌ BAD: N+1 問題
var users = await _context.Users.ToListAsync();
foreach (var user in users)
{
    var orders = user.Orders; // 每次迴圈都查詢
}

// ✅ GOOD: 使用 Include
var users = await _context.Users
    .Include(u => u.Orders)
    .ToListAsync();
```

### 使用 AsNoTracking

```csharp
// ✅ 唯讀查詢使用 AsNoTracking
var users = await _context.Users
    .AsNoTracking()
    .Where(u => u.IsActive)
    .ToListAsync();
```

### 避免在迴圈中 SaveChanges

```csharp
// ❌ BAD
foreach (var user in users)
{
    user.LastLogin = DateTime.UtcNow;
    await _context.SaveChangesAsync();
}

// ✅ GOOD
foreach (var user in users)
{
    user.LastLogin = DateTime.UtcNow;
}
await _context.SaveChangesAsync();
```

---

## 不可變性

### 使用 Records

```csharp
// ✅ DTOs 使用 record
public record UserDto(string Name, string Email);

// ✅ 使用 init-only properties
public class User
{
    public string Name { get; init; }
    public string Email { get; init; }
}

// ✅ 使用 with 建立新實例
var updatedUser = user with { Name = "New Name" };
```

---

## 禁止項目

### Console.WriteLine

```csharp
// ❌ 生產環境禁止
Console.WriteLine($"Processing user {userId}");

// ✅ 使用 ILogger
_logger.LogInformation("Processing user {UserId}", userId);
```

### Magic Numbers

```csharp
// ❌ BAD
if (retryCount > 3) { }

// ✅ GOOD
private const int MaxRetryCount = 3;
if (retryCount > MaxRetryCount) { }
```

### TODO/FIXME 沒有 Ticket

```csharp
// ❌ BAD
// TODO: fix this later

// ✅ GOOD
// TODO: JIRA-123 - Implement retry logic
```

---

## 審查嚴重度

### CRITICAL (90-100 分)

- 阻塞式 async 呼叫 (.Result, .Wait())
- 缺少 using/dispose 導致資源洩漏
- EF Core N+1 查詢在迴圈中

### HIGH (80-89 分)

- 方法超過 50 行
- 檔案超過 800 行
- 巢狀深度 > 4 層
- Console.WriteLine 殘留
- 缺少錯誤處理
- 缺少 CancellationToken

### MEDIUM (70-79 分)

- 命名不符合規範
- Magic numbers
- 缺少 XML 文件註解
- 使用 var 過度/不足

---

*版本：v1.0 | 更新日期：2026-01-29*
