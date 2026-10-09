---
name: tech-boundary-check
description: S3 技術邊界核對規則 B1–B8;對象是 S2 的 Component 與 Contract,每條輸出 PASS/WARN/FAIL + evidence
---

# 技術邊界核對規則

**全部由 `spec-dev.py check` 機械計算**(`specdev/rules.py`),LLM 不手填結果。輸入是 md 表格(Component、追溯、失敗模式、擁有權、測試),輸出每條規則對每個目標一筆 PASS/WARN/FAIL + evidence + action,寫入 `boundary-report.md` 與 `traceability.json.boundary_checks`。LLM 的工作是把資料填對,以及對 WARN/FAIL 決定處置。

## 規則表

| ID | 規則 | 適用目標 | FAIL 條件 | WARN 條件 |
|---|---|---|---|---|
| B1 | 每條需求經追溯表(AC→CMP)或 NFR 綁定映射到 ≥ 1 個 Component,且該 Component 有 layer 與 context | 每個 REQ、每條 AC | REQ 無 link,或 CMP 缺 layer/context | 某條 AC 沒指定由哪個 CMP 強制 |
| B2 | 依賴方向 `Api → Application → Domain ← Infrastructure`;Domain 不得依賴 Application/Infrastructure/Api;Application 不得依賴 Api/Infrastructure 具體型別 | 每個 CMP 的 `depends` | 反向依賴;depends 指向不存在的 CMP;layer 不在白名單 | Application → Infrastructure 且目標名稱欄沒寫 `: IInterface`;Api → Infrastructure |
| B3 | 跨 Bounded Context 只能經 Contract(API/Event),不得直接存取對方的 Repository 或資料表 | 每條跨 context 的 depends | 直接依賴他 context 的 Repository/Infrastructure CMP | 經 Application CMP 但無對應 API/Event 定義 |
| B4 | 外部系統呼叫只能出現在 Infrastructure 的 Adapter,且 `40-api-contracts.md` 有失敗模式(逾時/重試/降級/補償) | 每個 `external` 非空的 CMP | external 出現在非 Infrastructure 層 | 在 Infrastructure 但無失敗模式 |
| B5 | 每張資料表唯一 owner context | `50-data-model.md` 每張表 | 無 owner 或多 owner | — |
| B6 | NFR 落到具體 Component 或 API(例 P95 < 500ms 綁到 API-001) | 每個 NFR | — | 無對應 CMP/API |
| B7 | 每個 Component ≥ 1 個測試元件;每條 AC ≥ 1 個測試元件 | 每個 CMP、每條 AC | AC 無測試 | CMP 無測試 |
| B8 | 技術棧一致:Component 技術欄 ⊆ `stack` 值 + `tech_allowlist`(不分大小寫,前綴可)| 每個 CMP 的技術欄 | 非白名單且 method-log 無 `method=Spike.*` 且 `in` 含該 CMP | 有 Spike 但 `out` 不是 PASS/採用 |

## 結果格式

```json
{ "rule": "B2", "target": "CMP-003", "status": "FAIL",
  "evidence": "CMP-003 (Domain: Avatar aggregate) depends on CMP-005 (Infrastructure: BlobAdapter)",
  "action": "在 Domain 定義 IAvatarStorage 介面,BlobAdapter 實作之;Handler 經 DI 取得" }
```

`action` 在 WARN/FAIL 時必填。FAIL 阻擋 S4;WARN 放行但面板摘要計數。

## 從宣告到強制

B2/B3 在設計期查的是**宣告**。要讓它在程式碼上也成立,`60-test-design.md` 的「架構測試」表把同一條規則寫成 NetArchTest / ArchUnitNET 斷言,進 CI。否則面板綠了,程式碼還是會漂。

## 常見誤判

- Domain 依賴 MediatR 的 `INotification` 介面:算 WARN 不算 FAIL,但建議 Domain Event 用自家介面隔離。
- Application 依賴 `ILogger<T>`:抽象介面,PASS。
- 同一 context 內 Application 依賴 Infrastructure 的 Repository **介面**(定義在 Domain/Application):PASS;依賴具體類別:WARN。
