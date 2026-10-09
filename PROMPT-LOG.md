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

---

## P8(10-09)

> testcase可以做一份
> 英文/中文/中英混用
> senerio 1,  2, 3 (找商業變型)，全端1(重前、輕後)、全端2(輕前、重後)、全端3(均衡)、純前端，純後端
> 版本嗎？
> reviewer工具也要能在testcase驗收給我看(打開給我看)

> rd spec的首層是否為 : ui-spec, api-spec

> 分層該有的名詞對應轉換表，都要能查表(md)進行，才會快速

> ok(同意:首層共用核心、第二層 ui/ api/)

**產出**:2.4.0。
- **測試矩陣**:3 語言 × 3 商業情境(訂單取消退款 / 會議室預約 / 點數兌換)× 5 形狀,成對覆蓋 15 份完整專案,由產生器從情境資料產生,證據行號從產出的程式碼反查。每份 baseline + 3–4 個突變版(證據行號、反向依賴、無測試 AC、命名空間證據)。
- **雙語 spec**:章節與表頭中英別名,解析時正規化;英文斷詞(片語、詞形還原、片語動詞、狀態詞)。
- **分層結構**:首層共用核心,第二層 `ui/41-ui-spec.md`、`api/40`、`api/50`;依形狀可缺的檔不報。
- **分層命名對照表** `specs/naming-map.md`(+ 手寫覆寫):名詞 → 符號 → UI / API / Application / Domain / Infrastructure / DB,工具查表。
- **驗收板** `examples/matrix/_board/`。
**實測**:15/15 驗收、57/57 突變版被指定規則抓到、116 tests。斷詞召回 英 100% / 中 98% / 混 100%(中文有一部分來自受保護詞典,詞典裡的詞與情境重疊;「退款單」仍漏)。
**轉折**:矩陣第一次跑就抓到 reviewer 三個真缺陷,全是我自己剛加的功能造成的回歸 ——(1) 既有查詢 `GetOrder` 的證據行是 `GetOrderQueryHandler`,整字比對失敗 → 催生分層對照表;(2) 對照表跨層通查,`namespace Orders.Domain;` 因 DB 表名 `Orders` 被判成證據 → 改為證據所在層才比對;(3) survey 對應欄的命名空間片段被收進對照表 → 新增「命名空間證據」突變版,逼出點號串取最後一段。三次都是「變寬鬆以通過 baseline」的修法引入了假陰性,突變版是唯一能看見它的機制。

---

## P9(10-09)

> (手機截圖:REQ-002 分析鏈「SA 圖 0 · RD 圖 0」,三欄擠壓、行號溢出)
> 要有圖片啊
> 文字 對圖片
> 對文字

> 打開沒有照著mermaid繪出呀

> check board看轉換證據時，也可以查找glossary、docs目錄下的已知資產

**產出**:2.5.0。
- 每條需求卡改成 **PM 文字 ↔ 圖 ↔ RD 文字**,中間欄預設顯示兩張**自動生成**的圖(追溯圖、元件循序圖),不靠手寫,每條需求一定有圖;產生器也改成每條需求各有 ACT / SEQ-SA / SEQ / UC 流程圖。
- mermaid 改走 jsDelivr(npm 一對一鏡像,版本必存在),失敗改用 unpkg,兩者都失敗在頁面上提示;改為 mermaid 載入後才渲染;每張圖獨立渲染,語法錯誤就地標示。
- 新工具 `analyze.assets`:`docs/`、`specs/done/` 依標題切段建索引;每張卡列出相關的分層命名與文件段落;證據鏈頂端加查找框。
- 工具結果統一存 `ctx["carry"]`,重抽資料整包帶入(結束「glossary、lexicon 被洗掉」這類 bug 的根因)。
- 新增**真瀏覽器測試**:17 份面板逐一執行頁面 JavaScript,驗無 JS 錯誤、每條需求一張卡、每張預設圖都畫成 SVG、所有圖(含收合)可被 mermaid 解析、400px 不水平捲動、CDN 備援與失敗提示、查找框有結果。120 tests。
**轉折**:「沒畫出來」有三層原因,一層比一層深 ——(1) cdnjs 版本從未驗證;(2) 預設顯示的圖在 mermaid 下載完前就嘗試渲染,之後不再觸發;(3) 我重寫證據鏈區塊時刪掉了兩個函式,整個面板 JS 中斷 —— Python 測試只驗注入的資料,驗不到頁面腳本,所以 120 個綠燈之前其實一直有一個沒人執行過的頁面。補上瀏覽器測試後,又當場抓到兩個:循序圖訊息含分號(mermaid 語法字元)、testcase1 手寫 C4 圖一行多個 Rel(以前收在收合區沒人展開)。修窄螢幕時又自己在一行中間塞了 `//` 註解把程式碼吃掉,瀏覽器測試一跑 17 份全紅。

---

## P10(10-09)

> 結論
> - 用新版的建議寫法（E、F），1818 的真實落差每一種寫法都抓得到，G 也證明真的存在的東西會放行。紅燈、綠燈兩個方向都驗過了。
> - 剩下的限制是 B：如果不用字面鎖定、只寫函式名，還是會被騙過。這是比對名稱這種做法本身的極限，作者已經在閘門說明裡寫明「這是代理指標，不是行為存在的證明」。
> - 給團隊的用法建議：existing 和 modify 的證據一律加上字面鎖定，並指到能證明行為的那一行（例如運算子清單裡的那一項），不要指到函式宣告。
>
> 一個小問題：每條閘門結果在輸出裡印了兩次。一次是該 stage 的結果，一次是最後的總表，讀起來像有兩筆 finding。不影響判定，可以回報給作者。

> 簡單把你的核心閘門ssot列出來

**產出**:CLI 輸出改為 stage 只印各規則計數,總表每筆發現只列一次,INFO 預設收成計數(`--verbose` 看明細);新增「同一筆發現不得印兩次」測試。121 tests。回覆核心閘門 SSOT 清單。
**轉折**:使用者端的第一手驗證(1818,紅綠兩向)才是這個工具價值的證據;工具這邊能做的只是把「名稱比對是代理指標」寫進閘門說明,並把「字面鎖定 + 指行為行」變成團隊規範。

---

## P11(10-09)spec-reviewer 子系統 → 一站式審查

> 請強化 這個環節，足以形成一個spec-reviewer的子系統，要能做到我驗證、核對、審計圖片與來源/過程/目標

> 該子系統要能應用在所有的sa modeling後的結果

> 審計要優先能用看板確認 細節(與人類一起 )

> (附 file-explorer README)可以考慮設計成這樣的機制，但要特化給 spec review場景(PM, QA, RD共同核對)

> 好了沒啊

> The PM/QA/RD server design comes after this as a separate proposal. <--不應該separate，要一站式！

> 有時是跨職能同一個人，所以不用硬切不同人

> 是以事情要不要做來區分才對

> UML / 4C / event storming等圖型，是協助審計查詢用的，看板預設可以不用展開，點擊再開modal顯示某張圖片，某張表格就好，做成分頁彈性架構

> 名詞表也是

> 做好請下載給我

**產出**:
- S6 變成 spec-reviewer 子系統:自動圖(每條需求追溯圖 + 沿依賴走的元件循序圖)、mermaid 解析、核對函式庫、審計(來源 / 過程 / 目標 / hash / 歷史)、瀏覽器渲染驗證;規格可抽換(RD 依圖 ID 前綴、SA 依方法論檔 `steps[*].audit`)。
- 人工確認:**以事情區分**(是不是要的 / 測得出來 / 做得出來,`rules/review/duties.yaml`),同一人可一次做完;「不需要」要寫理由也算做完;hash 防護(簽到沒看過的版本會被拒、圖改了自動過期)。
- 一站式站台 `spec-dev.py serve`:同一張看板,直接確認、提問 / 回答、點「檔:行」看原文;唯一寫入 signoff.md、threads.md。
- 看板改成分頁彈性架構(`board.tabs`),圖 / 名詞表 / SA 表 / Survey 全表預設不展開,點晶片開 modal,modal 有分享連結。

**轉折**:
- 新的渲染驗證第一次跑就抓到看板 JS 壞了(證據鏈區塊被前一次編輯切掉一段)—— 這正是要做「看板也要被驗」的理由。
- 審計第一次跑矩陣,抓到**產生器自己畫的循序圖是一條直線**,和元件依賴表矛盾(8 種、40+ 筆 FAIL)。工具在驗我自己的產出。
- 站台的瀏覽器測試抓到原文抽屜的 CSS `display:flex` 蓋掉 `hidden`,抽屜永遠蓋在畫面上。
- 角色模型被使用者兩句話推翻:「同一個人可能跨職能」「以事情要不要做來區分」—— 以人分權是錯的抽象,事情才是審計的單位。
