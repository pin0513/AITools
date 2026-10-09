# rules — 規則資料層

規則是資料,不是程式。每條規則一個 YAML;程式(`tools/check/engine_v*.py`)只負責載入、呼叫 predicate、把 outcome 對到狀態與訊息。改嚴重度、改訊息、改參數、停用規則,都只改 YAML 或專案的 `.spec-dev.yaml`。

```
rules/
├── boundary/B1..B8.yaml     技術邊界規則(S3)
├── gates/G-*.yaml           Stage 放行規則(S0–S6)
├── methodology/routing.yaml 需求型態 → 方法論 M1–M18(S1/S2 的路由資料)
└── rulesets.yaml            啟用哪些規則、順序;專案覆寫範例
```

## 規則檔 schema

```yaml
id: B2                      # 唯一;boundary 用 B\d,gate 用 G-*
version: 1                  # 規則本身的版本;語意改了就 +1
category: boundary | gate
name: 依賴方向
description: 一句話
predicate: dependency_direction   # tools/check/predicates_v*.py 的函式名
inputs: [components]        # 讀 traceability 的哪些鍵(文件用,引擎不強制)
params: {...}               # 傳給 predicate;專案可覆寫
outcomes:                   # predicate 回傳的 outcome key → 狀態/訊息/處置
  reverse: {status: FAIL, message: "反向依賴:{from_layer} → {dep} ({to_layer})", action: "..."}
  allowed: {status: PASS, message: "{from_layer} → {dep} ({to_layer})"}
```

`status ∈ PASS | WARN | FAIL | INFO`。`message` / `action` 用 `{var}` 取 predicate 回傳的 `vars`。

## predicate 介面

```python
def dependency_direction(data: dict, params: dict, ctx: dict) -> list[dict]:
    # data = traceability(extract 產物);ctx = {"log", "live_log", "boundary", "config", "contracts"}
    return [{"outcome": "reverse", "target": "CMP-003", "ids": ["CMP-003", "CMP-005"], "vars": {...}}]
```

predicate 不決定嚴重度、不組訊息;它只回報「發生了哪種情況」。

## 專案覆寫(.spec-dev.yaml)

```yaml
rules:
  disable: [B8]
  overrides:
    B2:
      outcomes: { concrete_infra: { status: FAIL } }     # 升嚴
    B8:
      params: { extra_allowlist: [Polly, Hangfire] }
```

## 新增一條規則

1. 寫 `rules/<category>/<ID>.yaml`。
2. 在 `tools/check/predicates_v*.py` 加同名函式(或指向既有 predicate 換參數)。
3. 加進 `rulesets.yaml` 的 `default`。
4. 在 `tests/rules/cases/<ID>.yaml` 加至少一個 PASS 與一個非 PASS case。`tests/rules/test_rule_cases.py` 會自動跑。
