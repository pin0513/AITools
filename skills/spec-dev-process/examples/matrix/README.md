# 測試矩陣(產生物)

由 `tests/matrix/gen_matrix.py` 產生,不手改。驗收:`python3 spec-dev.py matrix examples/matrix`。

| ID | 形狀 | 語言 | 情境 | 元件 | 層 |
|---|---|---|---|---|---|
| fs-front-en-s1 | full-stack, front-heavy | en | s1 Order cancellation and refund | 11 | Api, ApiClient, Application, Component, Infrastructure, Page, Store |
| fs-front-zh-s2 | 全端(重前、輕後) | zh | s2 會議室預約 | 13 | Api, ApiClient, Application, Component, Infrastructure, Page, Store |
| fs-front-mixed-s3 | 全端(重前、輕後) | mixed | s3 會員點數兌換 | 11 | Api, ApiClient, Application, Component, Infrastructure, Page, Store |
| fs-back-en-s2 | full-stack, back-heavy | en | s2 Meeting room booking | 10 | Api, ApiClient, Application, Domain, Infrastructure, Page |
| fs-back-zh-s3 | 全端(輕前、重後) | zh | s3 會員點數兌換 | 9 | Api, ApiClient, Application, Domain, Infrastructure, Page |
| fs-back-mixed-s1 | 全端(輕前、重後) | mixed | s1 訂單取消與退款 | 9 | Api, ApiClient, Application, Domain, Infrastructure, Page |
| fs-balance-en-s3 | full-stack, balanced | en | s3 Loyalty points redemption | 12 | Api, ApiClient, Application, Component, Domain, Infrastructure, Page, Store |
| fs-balance-zh-s1 | 全端(均衡) | zh | s1 訂單取消與退款 | 12 | Api, ApiClient, Application, Component, Domain, Infrastructure, Page, Store |
| fs-balance-mixed-s2 | 全端(均衡) | mixed | s2 會議室預約 | 14 | Api, ApiClient, Application, Component, Domain, Infrastructure, Page, Store |
| fe-only-en-s1 | frontend only | en | s1 Order cancellation and refund | 5 | ApiClient, Component, Page, Store |
| fe-only-zh-s2 | 純前端 | zh | s2 會議室預約 | 6 | ApiClient, Component, Page, Store |
| fe-only-mixed-s3 | 純前端 | mixed | s3 會員點數兌換 | 5 | ApiClient, Component, Page, Store |
| be-only-en-s2 | backend only | en | s2 Meeting room booking | 8 | Api, Application, Domain, Infrastructure |
| be-only-zh-s3 | 純後端 | zh | s3 會員點數兌換 | 7 | Api, Application, Domain, Infrastructure |
| be-only-mixed-s1 | 純後端 | mixed | s1 訂單取消與退款 | 7 | Api, Application, Domain, Infrastructure |
