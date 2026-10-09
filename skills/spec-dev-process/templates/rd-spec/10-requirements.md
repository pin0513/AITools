# {feature-title} — 需求

## 需求清單
<!-- 型態:functional / state_heavy / domain_rich / data / integration(可多個,逗號分隔);非功能需求寫在下面的 NFR 表,不寫這裡 -->
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | | functional | PM§3.1 | AC-001-1, AC-001-2 |

## 驗收條件
```gherkin
# AC-001-1
Given 
When 
Then 
```

## 非功能需求
<!-- SEI Quality Scenario 六元素;「綁定 CMP/API」必填,否則 B6 WARN -->
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | | | | | | P95 < 500ms | API-001 | AC-N01-1 |

## 缺口(待 PM 確認)
<!-- PM spec 沒寫、你用假設補的,全部列這裡;method-log 對應筆的 evidence 必須是 assumed -->
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
