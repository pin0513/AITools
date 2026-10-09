# 會員點數兌換 (PM spec)

## 1 背景與目標
member 累積點數卻無法線上 redeem。目標:線上 redeem Reward,並維持可靠的點數帳本。

## 2 使用者與情境
member:想 redeem Reward 並 view PointTransaction。 system:讓舊點數 expire。

## 3 功能需求
### 3.1 PointsAccount 點數足夠時 member 可 redeem Reward
PointsAccount 餘額足夠時, member 可以 redeem Reward。 Redemption 初始為 Pending,扣點記為一筆 PointTransaction,由 RewardVendor 出貨。

### 3.2 點數 12 個月後 expire
12 個月未使用的點數會 expire。 system 每月排程寫一筆 expire PointTransaction,並扣減 PointsAccount 餘額。

### 3.3 member 可 view PointTransaction
member 可以 view 每筆 PointTransaction,含日期、類型與點數。

## 4 非功能需求
即使並行 redeem, PointsAccount 餘額也不得為負。

## 5 驗收條件
- 餘額足夠 → member redeem Reward → 建立 Redemption 並呼叫 RewardVendor
- 餘額不足 → member redeem Reward → 回應 422 INSUFFICIENT_POINTS,不扣點
- 點數於 13 個月前取得 → 每月排程執行 → 寫入 expire PointTransaction,餘額減少
- member 有 PointTransaction → member 開啟紀錄 → 每筆 PointTransaction 顯示日期、類型、點數
