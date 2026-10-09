# spec-reviewer

載入 `specs/rd/<issue>/spec`(RD spec)與 `specs/rd/<issue>/spec-review`(SA 素材、survey),跑 spec-dev-process 的 S0 → SA → SV → S1–S6,產生物寫回 spec-review。

```bash
specs/tools/spec-reviewer/review.sh issue-c            # 全部產出,退出碼 1 = 有 FAIL
specs/tools/spec-reviewer/review.sh issue-c --strict   # 依 pipeline stop_on 停
```

看什麼:`spec-review/check-panel.html`(SA 素材、survey、需求 × 元件 × 測試、邊界、log)。
