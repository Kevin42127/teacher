# Vercel 部署指南

## 部署步驟

### 1. 安裝 Vercel CLI

```bash
npm i -g vercel
```

### 2. 登入 Vercel

```bash
vercel login
```

### 3. 部署到 Vercel

```bash
vercel
```

### 4. 設定環境變數

在 Vercel 控制台中設定以下環境變數：

- `GROQ_API_KEY`: 您的 Groq API Key

### 5. 重要注意事項

⚠️ **Playwright 限制**：
- Playwright 在 Vercel Serverless Functions 中可能無法正常運作
- 因為 Playwright 需要下載瀏覽器二進制文件
- 建議考慮使用替代方案或調整架構

### 替代方案

如果 Playwright 無法在 Vercel 上運作，可以考慮：

1. **使用其他爬蟲庫**：
   - `requests` + `BeautifulSoup`（靜態內容）
   - `httpx` + `selectolax`（輕量級）

2. **使用外部服務**：
   - ScraperAPI
   - Bright Data
   - Apify

3. **部署到其他平台**：
   - Railway
   - Render
   - Fly.io
   - Google Cloud Run

## 檔案結構

```
.
├── api/
│   ├── __init__.py
│   ├── crawl.py          # 爬取 API
│   └── export.py         # 匯出 API
├── index.html            # 前端頁面
├── professor_crawler.py  # 爬蟲邏輯
├── requirements.txt      # Python 依賴
├── vercel.json          # Vercel 配置
└── .vercelignore        # 忽略檔案
```

## 測試部署

部署後，訪問您的 Vercel URL 測試功能。

