# {feature-title} Survey Mapping(模型 ↔ codebase)

候選看 `survey-candidates.md`(spec-dev.py 產生)。existing = 沿用;modify = 既有要改(證據 path:line);new = 不存在(不填證據)。

填寫規範:
- 模型元素用**程式碼裡的英文符號**(`FormSubmission`、`ApproveSubmissionCommandHandler`);中文放說明欄,或寫成「中文 (Symbol)」。純中文無符號 → WARN 請人確認,機器驗不了。
- existing / modify 的證據指到**能證明行為的那一行**,不要指到函式宣告;用 `path:line "字面文字"` 鎖定該行必須出現的文字(例:`Validator.cs:42 "FIELD_REQUIRED"`)。
- 這條驗證是代理指標:名字/文字出現在那一行 ≠ 功能存在。它抓「沒錨點」與「錨點指錯行」,抓不到「錨點對但宣稱錯」。

## 對應表
| 模型元素 | 類型 | 狀態 | 對應 codebase | 證據 | 說明 |
|---|---|---|---|---|---|
| Order | Aggregate | new | Orders.Domain.Order | | |
