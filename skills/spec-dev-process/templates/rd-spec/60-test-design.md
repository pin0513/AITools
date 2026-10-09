# {feature-title} — 測試設計

## 測試元件清單
<!-- TST = 測試類別(元件級),不是測試方法。kind ∈ unit / integration / contract / e2e。
     每條 AC ≥ 1 個 TST(B7 FAIL),每個 CMP ≥ 1 個 TST(B7 WARN) -->
| ID | 名稱 | kind | 對應 CMP | 對應 AC |
|---|---|---|---|---|
| TST-001 | DoFooCommandHandlerTests | unit | CMP-002 | AC-001-1 |
| TST-002 | FooAggregateTests | unit | CMP-003 | AC-001-2 |
| TST-003 | FooControllerTests | integration | CMP-001 | AC-001-1 |
| TST-004 | SqlFooRepositoryTests | integration | CMP-004 | AC-001-1 |
| TST-005 | FooLoadTest(k6) | e2e | CMP-001 | AC-N01-1 |

## Fitness Function
<!-- 每個 NFR 一列,否則 B6 WARN -->
| NFR | 量測方式 | 門檻 | 執行點 |
|---|---|---|---|
| NFR-001 | k6 load test API-001 | P95 < 500ms @ 100 VU | CI nightly |

## 架構測試
<!-- 把 B2/B3 的宣告變成可執行:NetArchTest / ArchUnitNET。規則與 config tech_boundary.dependency_direction 一致 -->
| 規則 | 工具 | 斷言 |
|---|---|---|
| B2 | NetArchTest | Types in Domain should not depend on Application/Infrastructure/Api |
