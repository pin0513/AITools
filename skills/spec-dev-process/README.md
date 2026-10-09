# spec-dev-process

PM spec → RD spec 的工程化轉換流程。可攜套件:**只需 python3(3.9+),零第三方相依**,整個資料夾就是一個 Claude Code skill,也可以純 CLI 使用。

```
spec-dev-process/
├── SKILL.md            Claude Code skill 入口(流程、LLM 規定、方法論路由)
├── config.yaml         流程能力設定(預設);專案用 .spec-dev.yaml 覆寫
├── spec-dev.py         CLI:init / extract / check / panel / render / all
├── specdev/            核心:md 解析、規則 B1–B8、報告、面板、渲染、YAML 子集解析
├── references/         方法論路由表、log 表示法、產出結構、邊界規則
├── templates/          rd-spec 7 個 md 模板 + check-panel.html
├── vendor/             mermaid.min.js 11.4.1(MIT)供 --offline
├── examples/avatar-upload/   完整範例(含刻意留的 FAIL/WARN)
├── tests/              python3 -m unittest discover tests
└── install.sh          連結或複製到 ~/.claude/skills/
```

## 安裝

```bash
# A. Claude Code skill(符號連結,之後 git pull 即更新)
./install.sh

# B. 複製一份(不想依賴原路徑)
./install.sh --copy

# C. 純 CLI,不裝 skill
python3 spec-dev.py all docs/rd-spec/<feature> --offline
```

`install.sh` 會檢查 python3 版本、跑一次測試、建立 `~/.claude/skills/spec-dev-process`。Windows 用 PowerShell:`New-Item -ItemType SymbolicLink -Path $HOME\.claude\skills\spec-dev-process -Target (Get-Location)`。

## 三分鐘走一遍

```bash
python3 spec-dev.py all examples/avatar-upload --offline
open examples/avatar-upload/check-panel.html     # macOS;Linux 用 xdg-open
```

預期輸出:退出碼 1,因為範例刻意留了 1 個 B2 FAIL、1 個 B7 FAIL、2 個 B8 FAIL。面板上每種狀態都看得到。

## 開一個新功能

```bash
python3 spec-dev.py init docs/rd-spec/order-cancel --title "訂單取消"
# LLM(或你)依 SKILL.md 填 7 個 md 與 method-log.jsonl
python3 spec-dev.py check docs/rd-spec/order-cancel     # 反覆跑到 0 FAIL
python3 spec-dev.py all   docs/rd-spec/order-cancel     # 產面板與 html
```

## 專案覆寫設定

在 repo 根目錄(或 rd-spec 目錄的任一上層)放 `.spec-dev.yaml`,只寫要改的頂層鍵:

```yaml
tech_boundary:
  layers: [Api, Application, Domain, Infrastructure]
  bounded_contexts: [Member, Order, Payment]
  stack: { language: C#, runtime: .NET, db: SQL Server, cache: Redis, messaging: MediatR, cloud: Azure }
  tech_allowlist: [ASP.NET Core, EF Core, StackExchange.Redis, xUnit, NSubstitute, FluentAssertions, NetArchTest, k6, Polly]
```

## 設計原則

| 原則 | 落實 |
|---|---|
| 單一事實來源 | 7 個 md 的表格;json/報告/面板全是產生物 |
| 能機械判定的不交給 LLM | B1–B8、孤兒、KPI 全在 `specdev/rules.py` |
| LLM 的判斷要留證據 | `method-log.jsonl` 每筆 `evidence ∈ explicit/inferred/assumed`;assumed 必須進缺口表 |
| 追溯到 AC | 追溯表 AC → CMP(職責),REQ 層由 AC 彙總 |
| 宣告要能變強制 | 架構測試表(NetArchTest)把 B2/B3 搬進 CI |

## 版本

見 `VERSION`。mermaid 11.4.1,授權見 `vendor/MERMAID-LICENSE`。
