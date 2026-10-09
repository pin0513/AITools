# spec-dev-process

PM spec → RD spec 的工程化轉換流程。可攜套件:**只需 python3(3.9+),零第三方相依**。整個資料夾就是一個 Claude Code skill,也可純 CLI 使用。

## 四層架構

```
spec-dev-process/
├── process/                 1. 骨幹:流程與 I/O 契約
│   ├── pipeline.yaml           S0–S6:owner(llm|tool)、inputs、outputs、tools@version、gates、stop_on
│   ├── io-contracts.yaml       每個檔要有的章節、表格簽名、必要欄;artifact 前綴;產生物清單
│   └── templates/              rd-spec 7 個 md 模板 + check-panel.html
├── tools/                   2. 工具:可迭代版本
│   ├── registry.yaml           name → {latest, versions{n: module[:fn]}};pipeline 以 name@n 引用
│   ├── analyze/extract_v1.py   md → traceability dict(含 spec-review 的 SA 素材與 survey)
│   ├── analyze/survey_v1.py    掃 codebase 產 survey 候選
│   ├── analyze/glossary_v1.py  跨 spec 詞彙表(名詞 ↔ 符號 ↔ 定義 ↔ 來源),衝突偵測
│   ├── check/engine_v1.py      規則引擎(載 YAML、呼叫 predicate、outcome → 狀態/訊息)
│   ├── check/predicates_v1.py  predicate 函式庫(只回報情況,不決定嚴重度)
│   ├── check/contract_v1.py    llm stage 產物契約檢查
│   ├── transform/              report / panel / render
│   └── execute/runner_v1.py    依 pipeline 跑 stage;init 骨架
├── rules/                   3. 規則資料層(YAML)
│   ├── boundary/B1..B8.yaml    技術邊界
│   ├── gates/G-*.yaml          Stage 放行
│   ├── methodology/routing.yaml 需求型態 → M1–M18
│   ├── methodology/sa/*.yaml   SA 建模方法論(可抽換;uml-wordbreak)
│   └── rulesets.yaml           啟用與順序;專案可 disable / overrides
├── tests/                   4. 測試
│   ├── unit/                   core、引擎、設定載入
│   ├── rules/cases/*.yaml      每條規則的資料驅動 case(引擎真的跑規則 YAML)
│   ├── contract/               四層引用一致(pipeline↔registry↔rules↔predicates↔contracts↔templates↔docs)
│   └── e2e/                    真的跑 CLI:範例、乾淨骨架、專案覆寫、嚴格停止
├── core/                    共用:md 解析、YAML 子集解析(有 PyYAML 優先)、設定/規則/流程載入
├── references/              人讀的方法論說明
├── examples/avatar-upload/  完整範例(刻意留 FAIL/WARN)
├── vendor/mermaid.min.js    11.4.1(MIT),--offline 內嵌
├── config.yaml / SKILL.md / spec-dev.py / install.sh / VERSION
```

```
          ┌──────────── process/pipeline.yaml ────────────┐
 stage →  │ owner=llm:契約檢查   owner=tool:registry 解析 │
          └───────┬──────────────────────┬────────────────┘
                  ▼                      ▼
        process/io-contracts.yaml   tools/*_vN.py ──► tools/check/engine ──► rules/*.yaml
                                                             │                    │
                                                        predicates_vN     outcome→status/message
```

## 安裝

```bash
./install.sh            # 檢查 python3 → 跑測試 → 符號連結到 ~/.claude/skills/
./install.sh --copy     # 複製一份
python3 spec-dev.py all docs/rd-spec/<feature> --offline     # 純 CLI
```

## 主流程(2.1)

PM 素材 → **SA Modeling**(可抽換方法論;斷詞 → 實體/關係 → 角色/流程 → UCD/ACT/SEQ/STM)→ **跨 spec 詞彙表**(`analyze.glossary` 合併所有 spec 的名詞 ↔ 符號,衝突另列)→ **Survey Mapping**(工具掃 codebase 出候選,定案後工具回 codebase 驗證證據;元素中英文皆可,中文經詞彙表 / SA2 解析符號)→ S1–S6 → check board(**證據鏈**:PM 原文/mock 內嵌 ↔ RD 片段附行號;**分析鏈**:方法論步驟與 UML,預設收合;**邏輯鏈**:每條需求命中的規則與證據;另有 SA 素材、survey、矩陣、邊界、log)→ 看板 → 改 md → 再跑。

端到端案例:`examples/testcase1-form-system/`(既有 codebase + issue c 走完整流程,`specs/tools/spec-reviewer/review.sh issue-c`)。

## 三分鐘走一遍

```bash
python3 spec-dev.py all examples/avatar-upload --offline   # 退出碼 1:範例刻意留 B2 / B7 FAIL
python3 spec-dev.py run examples/avatar-upload --to S6     # 嚴格模式:S3 FAIL 就停
python3 spec-dev.py rules; python3 spec-dev.py tools       # 看啟用規則與工具版本
python3 spec-dev.py glossary examples/testcase1-form-system/specs/rd/issue-c/spec   # 只抽跨 spec 詞彙表
```

## 開一個新功能

```bash
python3 spec-dev.py init docs/rd-spec/order-cancel --title "訂單取消"
# LLM(或你)依 SKILL.md 填 7 個 md 與 method-log.jsonl
python3 spec-dev.py check docs/rd-spec/order-cancel     # 反覆跑到 0 FAIL
python3 spec-dev.py all   docs/rd-spec/order-cancel     # 面板與 html
```

## 專案覆寫(.spec-dev.yaml,放 rd-spec 目錄任一上層)

```yaml
tech_boundary:
  bounded_contexts: [Member, Order, Payment]
  tech_allowlist: [ASP.NET Core, EF Core, StackExchange.Redis, xUnit, NSubstitute, NetArchTest, k6, Polly]
rules:
  disable: [B8]
  overrides:
    B2: { outcomes: { concrete_infra: { status: FAIL } } }
```

## 迭代方式

| 要改什麼 | 改哪裡 | 不用動 |
|---|---|---|
| 規則嚴重度 / 訊息 / 參數 | `rules/<cat>/<ID>.yaml` 或專案 overrides | 程式 |
| 新規則 | `rules/` 加 YAML + `tools/check/predicates_v1.py` 加函式 + `rulesets.yaml` + `tests/rules/cases/` | pipeline |
| 工具新版 | `tools/<cat>/<name>_v2.py` + `registry.yaml` 加版本 | 舊版繼續可釘 |
| 流程順序 / Gate / stop 行為 | `process/pipeline.yaml` | 工具 |
| 表格欄位 / 章節 | `process/io-contracts.yaml` + 模板 | extract(簽名驅動) |

## 測試

```bash
python3 -m unittest discover -s tests -t .        # 全部
python3 -m unittest tests.rules.test_rule_cases   # 只跑規則 case
```

## 版本

`VERSION` = 2.3.0。mermaid 11.4.1,授權見 `vendor/MERMAID-LICENSE`。
