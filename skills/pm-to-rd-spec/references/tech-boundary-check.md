---
name: tech-boundary-check
description: S3 技術邊界核對規則 B1–B8;對象是 S2 的 Component 與 Contract,每條輸出 PASS/WARN/FAIL + evidence
---

# 技術邊界核對規則

核對對象是設計產物(`traceability.json` 的 components / links / tests),不是程式碼。每條規則對每個適用目標各出一筆結果,寫入 `boundary_checks` 與 `boundary-report.md`。

## 規則表

| ID | 規則 | 適用目標 | FAIL 條件 | WARN 條件 |
|---|---|---|---|---|
| B1 | 每條需求映射到 ≥ 1 個 Component,且該 Component 有 layer 與 context | 每個 REQ | 無 link,或 link 到的 CMP 缺 layer/context | — |
| B2 | 依賴方向 `Api → Application → Domain ← Infrastructure`;Domain 不得依賴 Application/Infrastructure/Api;Application 不得依賴 Api/Infrastructure 具體型別 | 每個 CMP 的 `depends` | 出現反向依賴 | Application 直接依賴 Infrastructure(應經介面) |
| B3 | 跨 Bounded Context 只能經 Contract(API/Event),不得直接存取對方的 Repository 或資料表 | 每條跨 context 的 depends | 直接依賴他 context 的 Repository/Infrastructure CMP | 經 Application CMP 但無對應 API/Event 定義 |
| B4 | 外部系統呼叫只能出現在 Infrastructure 的 Adapter,且 `40-api-contracts.md` 有失敗模式(逾時/重試/降級/補償) | 每個 `external` 非空的 CMP | external 出現在非 Infrastructure 層 | 在 Infrastructure 但無失敗模式 |
| B5 | 每張資料表唯一 owner context | `50-data-model.md` 每張表 | 無 owner 或多 owner | — |
| B6 | NFR 落到具體 Component 或 API(例 P95 < 500ms 綁到 API-001) | 每個 NFR | — | 無對應 CMP/API |
| B7 | 每個 Component ≥ 1 個測試元件;每條 AC ≥ 1 個測試元件 | 每個 CMP、每條 AC | AC 無測試 | CMP 無測試 |
| B8 | 技術棧一致:Component 使用的技術 ⊆ `tech_boundary.stack` + 專案白名單 | 每個 CMP 的技術標註 | 用了非白名單技術且無 Spike 記錄 | 有 Spike 記錄但未結案 |

## 結果格式

```json
{ "rule": "B2", "target": "CMP-003", "status": "FAIL",
  "evidence": "CMP-003 (Domain: Avatar aggregate) depends on CMP-005 (Infrastructure: BlobAdapter)",
  "action": "在 Domain 定義 IAvatarStorage 介面,BlobAdapter 實作之;Handler 經 DI 取得" }
```

`action` 在 WARN/FAIL 時必填。FAIL 阻擋 S4;WARN 放行但面板摘要計數。

## 核對順序

B1 → B2 → B3 → B5 先跑(結構性);再 B4、B6、B8(屬性性);B7 最後(需要 S4 產物,S4 完成後回頭補跑)。

## 常見誤判

- Domain 依賴 MediatR 的 `INotification` 介面:算 WARN 不算 FAIL,但建議 Domain Event 用自家介面隔離。
- Application 依賴 `ILogger<T>`:抽象介面,PASS。
- 同一 context 內 Application 依賴 Infrastructure 的 Repository **介面**(定義在 Domain/Application):PASS;依賴具體類別:WARN。
