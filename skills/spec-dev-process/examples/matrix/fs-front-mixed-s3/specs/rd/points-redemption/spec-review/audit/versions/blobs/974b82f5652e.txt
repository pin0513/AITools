# 會員點數兌換 — requirements

## 需求清單
| ID | 需求 | 型態 | 來源錨點 | AC |
|---|---|---|---|---|
| REQ-001 | PointsAccount 點數足夠時 member 可 redeem Reward | functional, domain_rich, integration | PM§3.1 | AC-001-1, AC-001-2 |
| REQ-002 | 點數 12 個月後 expire | functional, data | PM§3.2 | AC-002-1 |
| REQ-003 | member 可 view PointTransaction | functional | PM§3.3 | AC-003-1 |

## 驗收條件
```gherkin
# AC-001-1
Given 餘額足夠
When member redeem Reward
Then 建立 Redemption 並呼叫 RewardVendor

# AC-001-2
Given 餘額不足
When member redeem Reward
Then 回應 422 INSUFFICIENT_POINTS,不扣點

# AC-002-1
Given 點數於 13 個月前取得
When 每月排程執行
Then 寫入 expire PointTransaction,餘額減少

# AC-003-1
Given member 有 PointTransaction
When member 開啟紀錄
Then 每筆 PointTransaction 顯示日期、類型、點數

```

## 非功能需求
| ID | 刺激 | 來源 | 環境 | 產物 | 回應 | 量測 | 綁定 CMP/API | AC |
|---|---|---|---|---|---|---|---|---|
| NFR-001 | 即使並行 redeem, PointsAccount 餘額也不得為負。 | user | normal load | API-001 | ok | balance never negative | API-001 | AC-N01-1 |

## 缺口(待 PM 確認)
| # | 問題 | 影響 REQ | 暫時假設 |
|---|---|---|---|
