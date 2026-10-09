# Prompt Log — spec-dev-process 這條線(2026-10-08 ~ 10-09)

供事後寫 paulfun 心得用。每一輪:你的原始 prompt(逐字)→ 這輪產出 → 關鍵轉折。未 commit,留在工作目錄。

---

## P1(10-08)

> 規劃一個軟體工程工作流程 流程能力設定
> Input : pm specs
> Support:md, mock system
>
> Output :
> rd specs
>
> Check System
> One page check  input and output and
> 軟體工程方法論 log 表示法 (default hide)
>
> 擅長把pm spec  轉換成 rd spec
> 轉換軟體工程方法論 表示法
> UML, 4C Model
> Stage file Format : mermaid +html
>
> 產出 依照 rd spec規範放置結構
> 依照技術邊界進行核對
>
> 核對面板包含 需求x技術元件x測試元件 矩陣
> 需求本身轉換時應該都有方法論 進行 分析與設計
>
> 核對面板上 除非要看才展開明細

**產出**:skill `pm-to-rd-spec` v1.0 — S0–S6 流程、config.yaml、方法論路由 M1–M17、B1–B8 邊界規則(文件)、8 個 md 模板、`build-check-panel.py`、一頁面板、範例。
**轉折**:「4C」解讀為 C4 model;面板驗證時發現 cdnjs 被 proxy 擋,改 npm 取 mermaid 做本機驗證,順手加 `--mermaid-js` 離線選項。

---

## P2(10-09)

> 覆盤一下，細節(uml)，核對用，核對al做法是否符合工程方法

**產出**:覆盤報告(只評估不動手)。抓到 5 個結構問題:可機械判定的規則交給 LLM 手填、無單一事實來源、AC→CMP 缺層、confidence 是貼標籤、字串比對狀態;UML 4 個:UI 狀態混進領域狀態機、UC 缺後置條件、Sequence 無例外 fragment、Aggregate 過度建模。
**轉折**:自己做的東西自己打;「證明,不要貼標籤」那條規則反過來打到 confidence 數字。

---

## P3(10-09)

> 產生一個portable spec-dev-process folder，讓我下載到另一個地方佈署

**產出**:`spec-dev-process` 1.1.0 可攜套件(零相依 CLI、md 表格為 SSOT、B1–B8 全由 script 算、AC 層級追溯、evidence 枚舉、vendor mermaid、install.sh、15 tests)。覆盤的 5+4 項全修。
**轉折**:「可攜」被解讀成「要修好再搬」,而不是把有已知缺陷的版本打包。

---

## P4(10-09)

> 把這份重構一下
> 1.設計執行階段骨幹與流程、input/output要求
> 2.工具(分析/轉換/執行/檢查)-可以迭代版本
> 3.規則資料層(rules)
> 4.測試

**產出**:2.0.0 四層架構 — `process/`(pipeline.yaml + io-contracts.yaml)、`tools/`(registry 管 name@version)、`rules/`(規則全 YAML,predicate 只回報 outcome)、`tests/`(unit / rules 資料驅動 / contract 跨層一致 / e2e)。72 tests。
**轉折**:規則「資料化」的邊界——嚴重度/訊息/參數是資料,判定邏輯仍是程式;contract test 專門抓四層之間的漂移。修到一個真 bug:stage 級 Gate 被面板誤用,KPI 與矩陣不一致。

---

## P5(10-09)

> main
> spec (all pm staffs)--> uml (sa modeling)  -> query and survey mapping (all input and codebase) --> rd spec
>
> sa modeling (可抽換方法論)
> 方法論a
> #uml => including   break word,  finding entity and relations , roles(角色、動作 、流程)
> ##core diagram for workflow
>    ###usecase diagram
>    ###activity diagram
>    ###sequence diagram
>    ###state diagrams
>     other diagram
>
> do -> sa modeling into next level specs(rd specs)
> and generate check board (要看的到所有素材、可以展開uml 圖當作分析 log圖)
> ->check all sa logs and diagram ,  looping
>
> 舉例
> testcase 1  表單系統
> testcase1
>    /src
>        web
>         api
>         database
>    /specs
>         /done
>             issue a
>             issue b
>          /in-progress
>             issue c
>           /rd
>                 /issue c
>                      /spec
>                       /spec-review
>           /tools
>                      /spec-reviewer (load spec-review folder)
>     /docs
>         /architecures
>         /guildelines
>
> 已經有: pm spec、mock web、參考文件
> RDSpec前已有: 即有codebase(有設計/前後端的example專案)
>
> 以要做issue c 為例子，做一次，驗證一次，證明一次

**產出**:2.1.0 — pipeline v2:S0 → SA(可抽換方法論,`rules/methodology/sa/uml-wordbreak.yaml` 七步)→ SV(`analyze.survey` 掃 codebase 出候選 + `G-SV-evidence` 打開檔案逐行驗證證據)→ S1–S6;check board 加 SA 素材區(圖可展開)與 Survey 區。testcase1 表單系統:既有 codebase(issue a/b)+ issue c 審核流程,走完整流程:7 個 SA 檔、19 個 survey 元素、RD spec 七檔、43/43 邊界 PASS、0 FAIL。
**轉折**:第一次跑 G-SV-evidence 就抓到我 survey 行號填錯(`SubmitFormCommandHandler.cs:11` 那行沒有符號)——驗證機制在第一個真實案例就證明了自己。「證明」用 e2e 做:獨立於規則引擎再把每條證據回 codebase 比對一次,並且把一條證據改壞、重跑、必須 FAIL(閉環)。

---

## P5 期間插入

> 請記下我的prompt，事後我要寫一個paulfun的心得~

→ 本檔。

> spec-viewer我的想象是要能載入
> 主要能在一個畫面中確認 ，PMSpec證據(文字+圖形  md/pic/...etc.  位置)   轉換 證據(uml圖-預設隱藏)   RDSpec證據

> 一個面板內確認(避免要切換畫面或app

> 除了sa modling workflow，最重要的就是那個面板了，證據鏈/分析鏈/邏輯鏈

**產出**:面板新增 E. 證據鏈主區:每條需求一列三欄 —— PM 證據(pm-spec 段落原文 + mock iframe/圖片內嵌,附 `檔案:行`)│ 分析鏈 ▸(`PM§3.1 ─[S1 UseCase·M1]→ UC-001 …` + SA 角色/實體 + UML)與 邏輯鏈 ▸(命中規則的狀態與證據)│ RD 證據(AC gherkin 原文、元件職責、測試、UC、API,各附行號)。另有「PM 素材全文」可展開。
**轉折**:第一版右欄整個不見——展開的 UML SVG 把表格撐寬把第三欄擠出可視區;「一個畫面內確認」這個要求在截圖裡被自己的圖打破,改固定欄寬 + SVG 限寬。NFR 的「來源」欄是 SEI 刺激來源不是 PM 錨點,要從來源對照表反查。

---

## P6(10-09)

> 這個工具的價值和限制
> - 有用的地方：「宣稱已有，就要附檔案與行號」這個規則，第一次試就抓到了 1818 那個真實落差。這正是審查報告 S-04、S-06 裡我自己犯的那類錯：只看代理物，沒看本體。
> - 要知道的限制：它驗的是「那一行有沒有出現這個名字」，不是「這個功能存不存在」（V6：代理指標不等於結論）。B 的寫法就能騙過它。中文命名的元素則永遠驗不過，而我們團隊的規格大量用中文命名。
> - 建議：
>   a. 元素名稱改用程式碼裡的英文符號，中文放說明欄。
>   b. 「existing」的證據改指到能證明行為的那一行（例如運算子清單裡的那一項），不要指到函式宣告。
>   c. 中文元素名一律 FAIL 這件事，可以回報給作者，請他改成「無可比對符號時標 WARN，請人確認」。
>
> 我自己填的值
> - 單項驗證挑 1818 的運算子，因為它是事先就知道答案的真實錯誤，適合當對照組。
> - 驗證放在 ~/.claude/jobs/4ffa675b/tmp/specdev-1818/，沒有寫進任何產品 repo。

> 1.必須中文、英文支援
> 2.跨spec需要抽取 glossary

**產出**:G-SV-evidence 改版 —— 證據支援 `path:line "字面文字"`(鎖定行為行,不只名字);元素符號解析順序 ASCII → 專案詞彙表 → 本 spec SA2 實體表,都解析不到 WARN「請人確認」而非 FAIL;規則 YAML 與文件明寫能力邊界(代理指標 ≠ 結論,抓「沒錨點 / 錨點指錯行」,抓不到「錨點對但宣稱錯」)。新工具 `analyze.glossary`:掃所有 `specs/rd/*/spec` 的名詞表、SA2、survey,合併為 `specs/glossary.md`(名詞 │ 符號 │ 定義 │ 來源 spec │ 檔:行)並列衝突;新 gate `G-GL-consistency`。testcase1 加 issue-b 名詞表回填,issue-c 兩個中文元素經詞彙表 / 字面文字驗過。102 tests。
**轉折**:使用者端的第一手驗證(1818)比我的 testcase1 更有說服力——它是事先知道答案的真實錯誤。「中文永遠驗不過」這個限制在我的範例裡根本不會出現,因為範例是我用英文寫的;這是作者盲點的典型例子。

---

## P7(10-09)

> 我認為sa modeling有一個前置解析層是
>
> 1. 自然語言(中/英) 切分斷詞 ，判斷動詞 名詞 做 角色 / 實體/ 關聯分析
> 2. 名詞/動作 詞頻出現率判斷，會作為glossary的重要性判斷
> 3. 後續分析就可以進行升級降級判斷。在繪圖 與 抓取 名詞會依此進行 glossary-mapping (spec/codebase nameing，透過工具層進行scan，避免全檔進ai model toke)

> 你同意嗎？

**回答**:方向同意,兩個前提要改 —— (1) 它是**候選產生器不是分類器**,LLM 仍要在 SA1 挑;(2) **詞頻是先驗不是結論**,降級不等於丟棄(「指派」只出現一次卻是缺口 #1 核心)。
**產出**:SA0 `analyze.lexicon`(pipeline `pre_tools`,零相依):中文功能字切分 + 2–5 字 n-gram + **邊界熵濾碎片** + 去冗;分類 狀態值 → 角色(摺疊動詞+角色片語)→ 動作 → 名詞;重要性 = 詞頻 × 章節權重 × 文件權重;名詞對詞彙表取符號並掃 codebase 命中;升/降級。詞典在 `rules/methodology/sa/lexicon-zh.yaml`。產出 `sa/00-lexicon.md` + `lexicon.json`,SA1 起只讀它。面板加 SA0 區。109 tests。
**實測**(對照人工 SA1):CJK 候選 325 → 邊界熵 111 → 去冗 104;召回 名詞 5/6、動作 7/7、角色 4/4;狀態值 4/4 正確。已知漏「待審清單」(待 被當切分字)。glossary-mapping 直接看出「審核紀錄 → ReviewRecord,codebase 0 命中」= new。
**轉折**:第一版沒有邊界熵,「醒審核者」「准或退回」這類 n-gram 碎片滿表;用無監督斷詞的標準手法(左右鄰字多樣性)一刀砍掉 2/3 候選。又踩到同一類 bug 第二次:後續 stage 重抽資料時把前面工具算的結果洗掉(glossary 一次、lexicon 一次)——這是 ctx 與 data 雙寫的結構問題,不是個案。
