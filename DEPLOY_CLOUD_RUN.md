# Google Cloud Run 部署指南

## 前置需求

1. Google Cloud 帳號
2. 安裝 Google Cloud SDK (gcloud)
3. 啟用 Cloud Run API

## 部署步驟

### 1. 安裝 Google Cloud SDK

**Windows:**
```powershell
# 下載並安裝 Google Cloud SDK
# https://cloud.google.com/sdk/docs/install
```

**驗證安裝:**
```bash
gcloud --version
```

### 2. 登入 Google Cloud

```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID
```

### 3. 啟用必要的 API

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### 4. 設定環境變數

在 Cloud Run 控制台中設定環境變數，或使用命令列：

```bash
gcloud run services update professor-crawler \
  --set-env-vars GROQ_API_KEY=your_groq_api_key \
  --region asia-east1
```

### 5. 建置並部署

#### 方法一：使用 Cloud Build（推薦）

```bash
gcloud builds submit --config cloudbuild.yaml
```

#### 方法二：手動建置和部署

```bash
# 建置 Docker 映像
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/professor-crawler

# 部署到 Cloud Run
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --max-instances 10
```

### 6. 取得服務 URL

部署完成後，會顯示服務 URL，例如：
```
https://professor-crawler-xxxxx-uc.a.run.app
```

## 配置說明

### 資源配置

- **Memory**: 2Gi（Playwright 需要較多記憶體）
- **CPU**: 2（處理爬蟲和 AI 請求）
- **Timeout**: 300 秒（爬取可能需要較長時間）
- **Max Instances**: 10（根據需求調整）

### 環境變數

在 Cloud Run 控制台或使用命令列設定：

```bash
GROQ_API_KEY=your_groq_api_key_here
```

## 本地測試 Docker 映像

```bash
# 建置映像
docker build -t professor-crawler .

# 執行容器
docker run -p 8080:8080 -e GROQ_API_KEY=your_key professor-crawler

# 測試
curl http://localhost:8080
```

## 更新部署

```bash
# 重新建置並部署
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/professor-crawler
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --region asia-east1
```

## 查看日誌

```bash
gcloud run services logs read professor-crawler --region asia-east1
```

## 成本估算

Cloud Run 按使用量計費：
- CPU: 每 vCPU 小時約 $0.00002400
- Memory: 每 GB 小時約 $0.00000250
- 請求: 前 200 萬次免費

## 注意事項

1. **Playwright 支援**: Cloud Run 支援 Playwright，但需要足夠的記憶體（建議 2Gi+）
2. **冷啟動**: 首次請求可能較慢（約 10-30 秒）
3. **超時限制**: 單一請求最長 300 秒（可調整）
4. **並發限制**: 根據配置的 CPU 和記憶體自動調整

## 故障排除

### 記憶體不足
```bash
# 增加記憶體
gcloud run services update professor-crawler \
  --memory 4Gi \
  --region asia-east1
```

### 超時問題
```bash
# 增加超時時間
gcloud run services update professor-crawler \
  --timeout 600 \
  --region asia-east1
```

### 查看錯誤日誌
```bash
gcloud run services logs read professor-crawler --region asia-east1 --limit 50
```

