# 資安弱點審查規則

完整的資安弱點審查規則，涵蓋 OWASP Top 10 和 .NET 特定安全議題。

---

## CRITICAL (90-100 分) - 必須修復

### 1. 硬編碼憑證

```csharp
// ❌ CRITICAL: 硬編碼 API Key
var apiKey = "sk-proj-xxxxx";
var openAiKey = "sk-xxxxx";

// ❌ CRITICAL: 硬編碼連線字串
var connectionString = "Server=prod;Password=secret123";

// ❌ CRITICAL: 硬編碼 Token
var bearerToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...";

// ❌ CRITICAL: 硬編碼密碼
var password = "P@ssw0rd123";
var adminPassword = "admin123";

// ✅ GOOD: 使用 Configuration
var apiKey = _configuration["OpenAI:ApiKey"];
var connectionString = _configuration.GetConnectionString("Default");

// ✅ BETTER: 使用 Azure Key Vault
var apiKey = await _keyVaultClient.GetSecretAsync("OpenAI-ApiKey");
```

**檢測模式：**
```regex
(password|pwd|secret|token|key|apikey|api_key|credential|conn.*string)\s*=\s*["'][^"']+["']
```

### 2. SQL 注入

```csharp
// ❌ CRITICAL: 字串串接 SQL
var query = $"SELECT * FROM Users WHERE Id = {userId}";
var query = "SELECT * FROM Users WHERE Name = '" + userName + "'";

// ❌ CRITICAL: ExecuteSqlRaw 串接
await _context.Database.ExecuteSqlRawAsync(
    $"DELETE FROM Users WHERE Id = {userId}");

// ✅ GOOD: 參數化查詢
var user = await _context.Users
    .Where(u => u.Id == userId)
    .FirstOrDefaultAsync();

// ✅ GOOD: ExecuteSqlRaw 參數
await _context.Database.ExecuteSqlRawAsync(
    "DELETE FROM Users WHERE Id = {0}", userId);
```

### 3. XSS 跨站腳本攻擊

```csharp
// ❌ CRITICAL: 直接輸出未編碼的使用者輸入
@Html.Raw(Model.UserComment)

// ❌ CRITICAL: JavaScript 中直接使用
<script>var name = '@Model.UserName';</script>

// ✅ GOOD: 使用 Razor 自動編碼
@Model.UserComment

// ✅ GOOD: 使用 JavaScript 編碼
<script>var name = '@Html.JavaScriptStringEncode(Model.UserName)';</script>
```

### 4. 不安全的反序列化

```csharp
// ❌ CRITICAL: BinaryFormatter (已棄用且危險)
var formatter = new BinaryFormatter();
var obj = formatter.Deserialize(stream);

// ❌ CRITICAL: TypeNameHandling.All
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.All
};

// ✅ GOOD: 使用 System.Text.Json
var obj = JsonSerializer.Deserialize<MyClass>(json);

// ✅ GOOD: 限制 TypeNameHandling
var settings = new JsonSerializerSettings
{
    TypeNameHandling = TypeNameHandling.None
};
```

### 5. 路徑遍歷

```csharp
// ❌ CRITICAL: 直接使用使用者輸入作為路徑
var filePath = Path.Combine(basePath, userInput);
var content = File.ReadAllText(filePath);

// ❌ CRITICAL: 可能的路徑遍歷
var fileName = request.FileName; // 可能是 "../../../etc/passwd"
var path = $"/uploads/{fileName}";

// ✅ GOOD: 驗證並清理路徑
var fileName = Path.GetFileName(userInput); // 移除路徑
var safePath = Path.Combine(basePath, fileName);
if (!safePath.StartsWith(basePath))
{
    throw new SecurityException("Invalid path");
}
```

### 6. 敏感資料洩漏

```csharp
// ❌ CRITICAL: 在 log 中輸出密碼
_logger.LogInformation("User login: {Password}", password);

// ❌ CRITICAL: 在 log 中輸出 token
_logger.LogDebug("API response: {Token}", apiToken);

// ❌ CRITICAL: 錯誤訊息洩漏堆疊
return StatusCode(500, ex.ToString());

// ✅ GOOD: 遮蔽敏感資料
_logger.LogInformation("User login attempt for {UserId}", userId);

// ✅ GOOD: 通用錯誤訊息
return StatusCode(500, "An error occurred");
```

---

## HIGH (80-89 分) - 強烈建議修復

### 7. 缺少輸入驗證

```csharp
// ❌ HIGH: 未驗證的使用者輸入
public async Task<IActionResult> CreateUser(CreateUserDto dto)
{
    var user = new User { Email = dto.Email }; // 未驗證
    await _repository.AddAsync(user);
}

// ✅ GOOD: 使用 DataAnnotations
public class CreateUserDto
{
    [Required]
    [EmailAddress]
    [StringLength(100)]
    public string Email { get; set; }
}

// ✅ GOOD: 使用 FluentValidation
public class CreateUserValidator : AbstractValidator<CreateUserDto>
{
    public CreateUserValidator()
    {
        RuleFor(x => x.Email).NotEmpty().EmailAddress();
    }
}
```

### 8. 缺少授權檢查

```csharp
// ❌ HIGH: 缺少 [Authorize] attribute
public class AdminController : Controller
{
    public async Task<IActionResult> DeleteUser(int id) { }
}

// ❌ HIGH: 缺少資源層級授權
public async Task<IActionResult> GetOrder(int orderId)
{
    var order = await _repository.GetByIdAsync(orderId);
    return Ok(order); // 沒檢查是否屬於當前使用者
}

// ✅ GOOD: 加上授權
[Authorize(Roles = "Admin")]
public class AdminController : Controller { }

// ✅ GOOD: 資源層級授權
public async Task<IActionResult> GetOrder(int orderId)
{
    var order = await _repository.GetByIdAsync(orderId);
    if (order.UserId != CurrentUserId)
        return Forbid();
    return Ok(order);
}
```

### 9. CSRF 缺少保護

```csharp
// ❌ HIGH: POST 方法缺少 AntiForgeryToken
[HttpPost]
public async Task<IActionResult> TransferMoney(TransferDto dto)
{
    await _service.TransferAsync(dto);
    return Ok();
}

// ✅ GOOD: 加上 ValidateAntiForgeryToken
[HttpPost]
[ValidateAntiForgeryToken]
public async Task<IActionResult> TransferMoney(TransferDto dto)
{
    await _service.TransferAsync(dto);
    return Ok();
}
```

### 10. 不安全的隨機數

```csharp
// ❌ HIGH: 使用 Random 產生安全相關數值
var random = new Random();
var token = random.Next().ToString();

// ✅ GOOD: 使用加密安全隨機數
using var rng = RandomNumberGenerator.Create();
var bytes = new byte[32];
rng.GetBytes(bytes);
var token = Convert.ToBase64String(bytes);
```

### 11. 密碼儲存不當

```csharp
// ❌ HIGH: 明文儲存密碼
user.Password = password;

// ❌ HIGH: 使用 MD5/SHA1
user.Password = ComputeMD5(password);

// ✅ GOOD: 使用 BCrypt 或 Argon2
user.PasswordHash = BCrypt.HashPassword(password);

// ✅ GOOD: 使用 ASP.NET Core Identity
var result = await _userManager.CreateAsync(user, password);
```

---

## MEDIUM (70-79 分) - 建議修復

### 12. 缺少 HTTPS 強制

```csharp
// ❌ MEDIUM: 未強制 HTTPS
app.UseRouting();

// ✅ GOOD: 強制 HTTPS
app.UseHttpsRedirection();
app.UseHsts();
```

### 13. 缺少安全 Headers

```csharp
// ✅ GOOD: 加上安全 Headers
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    await next();
});
```

### 14. Cookie 安全設定

```csharp
// ❌ MEDIUM: 不安全的 Cookie 設定
services.ConfigureApplicationCookie(options =>
{
    options.Cookie.HttpOnly = false;
    options.Cookie.SecurePolicy = CookieSecurePolicy.None;
});

// ✅ GOOD: 安全的 Cookie 設定
services.ConfigureApplicationCookie(options =>
{
    options.Cookie.HttpOnly = true;
    options.Cookie.SecurePolicy = CookieSecurePolicy.Always;
    options.Cookie.SameSite = SameSiteMode.Strict;
});
```

---

## 檢測清單

### 必須檢查的關鍵字

```
敏感資料:
- password, pwd, secret, token, key, apikey, api_key
- credential, connectionstring, conn_string
- private_key, client_secret, access_token

危險函式:
- ExecuteSqlRaw, FromSqlRaw (不帶參數)
- BinaryFormatter, Deserialize
- Html.Raw, @Html.Raw
- File.ReadAllText, File.WriteAllText (使用者輸入)

缺失驗證:
- 缺少 [Authorize]
- 缺少 [ValidateAntiForgeryToken]
- 缺少 [Required], [StringLength]
```

### 檔案類型優先順序

1. **最高優先**: Controllers, API endpoints
2. **高優先**: Services, Repositories
3. **中優先**: Models, DTOs
4. **低優先**: Tests, Utilities

---

## 審查輸出格式

```markdown
### 🔴 CRITICAL - 安全弱點

**[SEC-001] 硬編碼 API Key**
- **File:** src/Services/PaymentService.cs:45
- **Issue:** 發現硬編碼的 Stripe API key
- **Evidence:** `var apiKey = "sk_live_xxx..."`
- **Risk:** API key 洩漏可能導致財務損失
- **Fix:** 使用 Configuration 或 Key Vault
- **OWASP:** A3:2017 - Sensitive Data Exposure

**[SEC-002] SQL 注入風險**
- **File:** src/Repositories/UserRepository.cs:78
- **Issue:** 使用字串串接建構 SQL 查詢
- **Evidence:** `$"SELECT * FROM Users WHERE Id = {id}"`
- **Risk:** 攻擊者可執行任意 SQL
- **Fix:** 使用參數化查詢或 EF Core LINQ
- **OWASP:** A1:2017 - Injection
```

---

*版本：v1.0 | 更新日期：2026-01-29*
