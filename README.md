# 大學教授資料採集系統

專業的網頁爬蟲工具，用於採集大學網站上的教授資訊（姓名、Email、科系），支援匯出為 CSV 格式。

## 功能特點

- 🎯 智能解析多種大學網站結構
- 📊 支援 CSV 格式匯出
- 🌐 支援臺灣及國際大學網站
- ⚡ 多執行緒並行處理提升效率
- 🎨 現代化網頁操作介面
- 🔍 即時預覽採集結果

## 本地開發

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 啟動應用

```bash
python app.py
```

開啟瀏覽器訪問: `http://localhost:5000`

## Google Cloud Run 部署（推薦 - 支援完整功能）

### 部署步驟

1. **安裝 Google Cloud SDK**
   - 下載：https://cloud.google.com/sdk/docs/install
   - 或使用：`gcloud components install`

2. **登入 Google Cloud**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

3. **啟用必要的 API**
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

4. **使用 Cloud Build 部署**
```bash
gcloud builds submit --config cloudbuild.yaml
```

### 或使用 gcloud 直接部署

```bash
# 構建並推送映像
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/professor-scraper

# 部署到 Cloud Run
gcloud run deploy professor-scraper \
  --image gcr.io/YOUR_PROJECT_ID/professor-scraper \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 300
```

### Cloud Run 優勢

✅ **完整功能支援**：
- ✅ 支援 Selenium 和 Chrome（已配置）
- ✅ 支援深度爬蟲功能
- ✅ 完整 Python 環境
- ✅ 免費額度（每月 200 萬請求）
- ✅ 自動擴展到零（不計費）
- ✅ 自動 HTTPS
- ✅ 全球多區域部署
- ✅ 企業級可靠性

### 價格

- **免費額度**: 
  - 每月 200 萬請求
  - 360,000 GB-秒記憶體
  - 180,000 vCPU-秒
- **超出後**: 按使用量計費
- **預估**: 輕量使用可能完全免費

### 配置說明

專案已包含：
- `Dockerfile` - 自動安裝 Chrome 和依賴
- `cloudbuild.yaml` - Cloud Build 配置文件
- `.dockerignore` - Docker 構建優化
- 所有深度爬蟲功能已就緒

### 常用命令

```bash
# 查看服務狀態
gcloud run services list

# 查看日誌
gcloud run services logs read professor-scraper --region asia-east1

# 更新服務
gcloud run deploy professor-scraper --image gcr.io/YOUR_PROJECT_ID/professor-scraper

# 刪除服務
gcloud run services delete professor-scraper --region asia-east1
```

## Vercel 部署（功能受限）

### 部署步驟

1. **安裝 Vercel CLI**（如果尚未安裝）
```bash
npm i -g vercel
```

2. **登入 Vercel**
```bash
vercel login
```

3. **部署到 Vercel**
```bash
vercel
```

4. **生產環境部署**
```bash
vercel --prod
```

### 注意事項

⚠️ **重要限制**：
- Vercel serverless 環境不支援 Selenium
- 深度爬蟲功能（點擊連結進入詳細頁面）在 Vercel 上無法使用
- 僅支援靜態 HTML 頁面的直接採集

## 使用方式

1. 在輸入框貼上大學系所網頁 URL
2. 點擊「開始採集」按鈕
3. 等待處理完成後查看結果
4. 點擊「匯出 Excel」下載 CSV 檔案

## 技術棧

- Backend: Python + Flask
- Frontend: HTML5 + CSS3 + JavaScript
- 爬蟲: BeautifulSoup4
- 資料處理: Pandas

## 支援的網站類型

- 臺灣各大學系所網站
- 教師介紹頁面
- 師資陣容列表
- 通用學術網站結構
