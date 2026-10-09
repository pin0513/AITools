# 會員點數兌換 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | 點數帳戶點數足夠時會員可兌換獎品 | functional, domain_rich, integration | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 點數 12 個月後到期 | functional, data | PM§3.2 | AC-002-1 |
| REQ-003 | 會員可查看點數交易 | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given 餘額足夠
When 會員兌換獎品
Then 建立兌換單並呼叫獎品供應商

# AC-001-2
Given 餘額不足
When 會員兌換獎品
Then 回應 422 INSUFFICIENT_POINTS,不扣點

# AC-002-1
Given 點數於 13 個月前取得
When 每月排程執行
Then 寫入到期點數交易,餘額減少

# AC-003-1
Given 會員有點數交易
When 會員開啟紀錄
Then 每筆點數交易顯示日期、類型、點數

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 即使並行兌換,點數帳戶餘額也不得為負。 | user | normal load | API-001 | ok | balance never negative | API-001 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
