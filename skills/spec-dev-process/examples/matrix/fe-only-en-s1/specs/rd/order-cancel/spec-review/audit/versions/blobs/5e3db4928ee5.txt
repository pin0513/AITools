# order-cancel SA0 前置解析(由 analyze.lexicon 產生,不手改;SA1 從這裡挑,不必讀整份原文)

來源:pm_spec:pm-spec.md, mock:order.html, ref:refs.md · CJK 候選 0 → 邊界熵後 0 → 去冗後 0

規則:詞頻 × 章節權重 × 文件權重 = 重要性(先驗,不是結論)。**降級不等於丟棄**:SA1 撿回降級詞要在 01-break-words 的歸類欄寫理由。

## 名詞候選

| 詞 | 詞頻 | 權重 | 詞彙表符號 | codebase 命中 | 建議 | 出現 |
|---|---|---|---|---|---|---|
| order | 21 | 21.0 | Order | 3 (src/web/src/types/Order.ts:4) | 升 | mock:order.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A custom |
| payment gateway | 5 | 5.0 | PaymentGateway | 0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| issues | 4 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| status | 4 | 4.0 |  | — | 升 | mock:order.html pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§5 Acceptance |
| support | 4 | 4.0 |  | — | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§5 Acceptance |
| cancellation | 3 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§4 Non-functi |
| history | 3 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§5 Acceptance |
| order status | 3 | 3.0 |  | — | 升 | mock:order.html pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§5 Acceptance |
| system issues | 3 | 3.0 |  | — | 升 | pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| times | 3 | 3.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| cancellation history | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 A suppor |
| order records | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§4 Non-functi pm_spec:pm-spec.md§5 Acceptance |
| reason | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§5 Acceptance |
| retries | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| through | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§3.2 The syst |
| time | 2 | 2.0 |  | — | 降 | pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§5 Acceptance |

## 動作候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| cancel | 8 | 8.0 | 升 | mock:order.html pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A custom |
| refund | 7 | 7.0 | 降 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§4 Non-functi |
| view | 2 | 2.0 | 降 | mock:order.html pm_spec:pm-spec.md§3.3 A suppor |

## 角色候選

| 詞 | 詞頻 | 權重 | 建議 | 出現 |
|---|---|---|---|---|
| customer | 5 | 5.0 | 升 | pm_spec:pm-spec.md§1 Background pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§5 Acceptance |
| system | 5 | 5.0 | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| support agent | 3 | 3.0 | 降 | pm_spec:pm-spec.md§2 Users pm_spec:pm-spec.md§3.3 A suppor pm_spec:pm-spec.md§5 Acceptance |

## 狀態值候選(屬性,不建實體)

| 詞 | 詞頻 | 出現 |
|---|---|---|
| cancelled | 8 | pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |
| placed | 3 | mock:order.html pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§5 Acceptance |
| shipped | 3 | pm_spec:pm-spec.md§3.1 A custom pm_spec:pm-spec.md§5 Acceptance |
| refunded | 2 | pm_spec:pm-spec.md§3.2 The syst pm_spec:pm-spec.md§5 Acceptance |

## 英文符號

| 符號 | 詞頻 | codebase 命中 | 出現 |
|---|---|---|---|
| order | 20 | 3 (src/web/src/types/Order.ts:4) | mock:order.html pm_spec:pm-spec.md |
| cancelled | 8 | 0 | pm_spec:pm-spec.md |
| refund | 7 | 0 | pm_spec:pm-spec.md |
| cancel | 6 | 0 | mock:order.html pm_spec:pm-spec.md |
| customer | 5 | 0 | pm_spec:pm-spec.md |
| gateway | 5 | 0 | pm_spec:pm-spec.md |
| payment | 5 | 0 | pm_spec:pm-spec.md |
| system | 5 | 0 | pm_spec:pm-spec.md |
| issues | 4 | 0 | pm_spec:pm-spec.md |
| status | 4 | 1 (src/web/src/types/Order.ts:6) | mock:order.html pm_spec:pm-spec.md |
| support | 4 | 0 | pm_spec:pm-spec.md |
| agent | 3 | 0 | pm_spec:pm-spec.md |
| cancellation | 3 | 0 | pm_spec:pm-spec.md |
| history | 3 | 0 | pm_spec:pm-spec.md |
| times | 3 | 0 | pm_spec:pm-spec.md |
| After | 2 | 0 | pm_spec:pm-spec.md |
| cancels | 2 | 0 | pm_spec:pm-spec.md |
| must | 2 | 0 | pm_spec:pm-spec.md |
| placed | 2 | 1 (src/web/src/types/Order.ts:2) | pm_spec:pm-spec.md |
| reason | 2 | 0 | pm_spec:pm-spec.md |
| records | 2 | 0 | pm_spec:pm-spec.md |
| refunded | 2 | 0 | pm_spec:pm-spec.md |
| retries | 2 | 0 | pm_spec:pm-spec.md |
| shipped | 2 | 1 (src/web/src/types/Order.ts:2) | pm_spec:pm-spec.md |
| through | 2 | 0 | pm_spec:pm-spec.md |
| time | 2 | 0 | pm_spec:pm-spec.md |
| view | 2 | 0 | mock:order.html pm_spec:pm-spec.md |
| Goal | 1 | 0 | pm_spec:pm-spec.md |
| ORDER_SHIPPED | 1 | 0 | pm_spec:pm-spec.md |
| Placed | 1 | 1 (src/web/src/types/Order.ts:2) | mock:order.html |
| Today | 1 | 0 | pm_spec:pm-spec.md |
| When | 1 | 0 | pm_spec:pm-spec.md |
| after | 1 | 0 | pm_spec:pm-spec.md |
| already | 1 | 0 | pm_spec:pm-spec.md |
| automatic | 1 | 0 | pm_spec:pm-spec.md |
| becomes | 1 | 0 | pm_spec:pm-spec.md |
| called | 1 | 0 | pm_spec:pm-spec.md |
| cannot | 1 | 0 | pm_spec:pm-spec.md |
| each | 1 | 0 | pm_spec:pm-spec.md |
| every | 1 | 0 | pm_spec:pm-spec.md |
