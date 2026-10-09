# testcase1 — 表單系統

spec-dev-process 的端到端測試案例。既有 codebase(issue a/b 已完成)+ 新需求 issue c(表單審核流程)。

```
src/        web(React)、api(.NET: Api/Application/Domain/Infrastructure)、database(SQL)
specs/
  done/           issue-a 表單建立、issue-b 表單填寫(已上線)
  in-progress/    issue-c:PM spec、mock、參考文件(輸入)
  rd/issue-c/
    spec/         RD spec(7 個 md + method-log)← 唯一事實來源
    spec-review/  SA 建模素材(sa/01..07)、survey-mapping.md、check board 與報告(產生物)
  tools/spec-reviewer/   載入 spec-review 跑核對
docs/       architectures、guidelines
.spec-dev.yaml   專案覆寫(review_dir、方法論、survey 範圍、技術白名單)
```

跑法:

```bash
specs/tools/spec-reviewer/review.sh issue-c [--offline]   # = spec-dev.py all specs/rd/issue-c/spec
open specs/rd/issue-c/spec-review/check-panel.html
```
