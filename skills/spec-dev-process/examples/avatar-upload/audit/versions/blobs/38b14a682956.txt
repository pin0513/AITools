# 會員上傳大頭貼 — 概觀

## 背景與目標
會員目前只有預設頭像。PM§1:提供上傳大頭貼,目標是個人頁完成度(有頭像會員比例)三個月內從 0 提升到 40%。

## 範圍
| In | Out |
|---|---|
| 上傳 jpg/png ≤ 5MB、裁切正方形、個人頁顯示 | GIF 動圖、AI 生成頭像、頭像審核流程 |

## 名詞表
| 名詞 | 定義 | 來源 |
|---|---|---|
| 大頭貼 | 會員個人頁顯示的正方形圖片 | PM§2 |
| SAS | Azure Blob 的限時存取簽章 URL | PM§4 |

## 來源對照
| PM 來源 | RD 產物 |
|---|---|
| PM§1 背景與目標 | 00-overview.md |
| PM§3.1 上傳大頭貼 | REQ-001, UC-001, SEQ-001 |
| PM§3.2 圖片裁切 | REQ-002, UC-002, STM-UI-001 |
| PM§3.3 顯示於個人頁 | REQ-003, UC-003 |
| PM§4 非功能需求 | NFR-001, NFR-002 |
| mock/avatar/upload.html | STM-UI-001(idle/cropping/uploading/done), 欄位: file, cropBox |
