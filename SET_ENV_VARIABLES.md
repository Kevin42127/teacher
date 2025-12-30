# 設置環境變數指南

## Google Cloud Run 環境變數設置

### 方法一：使用 Google Cloud Console（圖形介面）

1. **登入 Google Cloud Console**
   - 訪問：https://console.cloud.google.com
   - 選擇您的專案

2. **進入 Cloud Run 服務**
   - 在左側選單找到「Cloud Run」
   - 點擊您的服務名稱（例如：`professor-crawler`）

3. **編輯服務**
   - 點擊「編輯和部署新版本」按鈕

4. **設置環境變數**
   - 向下滾動找到「變數和密鑰」區塊
   - 點擊「新增變數」
   - 輸入以下資訊：
     - **名稱**: `GROQ_API_KEY`
     - **值**: 您的 Groq API Key（例如：`gsk_...`）
   - 點擊「部署」按鈕

### 方法二：使用 gcloud 命令列

#### 在部署時設置

```bash
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars GROQ_API_KEY=your_groq_api_key_here
```

#### 更新現有服務的環境變數

```bash
# 設置單一環境變數
gcloud run services update professor-crawler \
  --set-env-vars GROQ_API_KEY=your_groq_api_key_here \
  --region asia-east1

# 設置多個環境變數
gcloud run services update professor-crawler \
  --set-env-vars GROQ_API_KEY=your_key,ANOTHER_VAR=another_value \
  --region asia-east1

# 從檔案讀取環境變數
gcloud run services update professor-crawler \
  --env-vars-file .env.yaml \
  --region asia-east1
```

#### 使用環境變數檔案（.env.yaml）

建立 `.env.yaml` 檔案：

```yaml
GROQ_API_KEY: "your_groq_api_key_here"
```

然後使用：

```bash
gcloud run services update professor-crawler \
  --env-vars-file .env.yaml \
  --region asia-east1
```

### 方法三：使用 Secret Manager（推薦用於敏感資訊）

#### 1. 建立 Secret

```bash
# 建立 Secret
echo -n "your_groq_api_key_here" | gcloud secrets create groq-api-key \
  --data-file=-

# 或從檔案建立
gcloud secrets create groq-api-key \
  --data-file=path/to/your/key.txt
```

#### 2. 授予 Cloud Run 服務帳號權限

```bash
# 取得服務帳號
PROJECT_NUMBER=$(gcloud projects describe YOUR_PROJECT_ID --format="value(projectNumber)")
SERVICE_ACCOUNT="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

# 授予權限
gcloud secrets add-iam-policy-binding groq-api-key \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

#### 3. 在部署時使用 Secret

```bash
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --platform managed \
  --region asia-east1 \
  --update-secrets GROQ_API_KEY=groq-api-key:latest
```

## 驗證環境變數

### 檢查已設置的環境變數

```bash
gcloud run services describe professor-crawler \
  --region asia-east1 \
  --format="value(spec.template.spec.containers[0].env)"
```

### 在應用程式中測試

在您的 Python 代碼中：

```python
import os
api_key = os.getenv('GROQ_API_KEY')
if api_key:
    print("環境變數已設置")
else:
    print("環境變數未設置")
```

## 更新環境變數

### 更新現有變數

```bash
gcloud run services update professor-crawler \
  --update-env-vars GROQ_API_KEY=new_value \
  --region asia-east1
```

### 刪除環境變數

```bash
gcloud run services update professor-crawler \
  --remove-env-vars GROQ_API_KEY \
  --region asia-east1
```

## 本地開發環境變數

### 使用 .env 檔案

在專案根目錄建立 `.env` 檔案：

```
GROQ_API_KEY=your_groq_api_key_here
```

確保 `.env` 在 `.gitignore` 中，避免提交到 Git。

### 在本地測試

```bash
# 使用環境變數執行
export GROQ_API_KEY=your_key
python app.py

# 或使用 .env 檔案（python-dotenv 會自動載入）
python app.py
```

## 安全建議

1. **不要將 API Key 提交到 Git**
   - 確保 `.env` 在 `.gitignore` 中
   - 不要在程式碼中硬編碼 API Key

2. **使用 Secret Manager**
   - 對於生產環境，建議使用 Google Secret Manager
   - 更安全且易於管理

3. **定期輪換 API Key**
   - 定期更新 API Key
   - 使用 Secret Manager 可以輕鬆更新

4. **限制權限**
   - 只授予必要的服務帳號權限
   - 使用最小權限原則

## 常見問題

### Q: 環境變數設置後不生效？
A: 
- 確認服務已重新部署
- 檢查變數名稱是否正確（大小寫敏感）
- 查看服務日誌確認

### Q: 如何查看環境變數？
A: 使用 `gcloud run services describe` 命令或 Cloud Console

### Q: 可以設置多少個環境變數？
A: Cloud Run 支援最多 32KB 的環境變數總大小

## 快速參考

```bash
# 設置環境變數
gcloud run services update SERVICE_NAME \
  --set-env-vars KEY=VALUE \
  --region REGION

# 更新環境變數
gcloud run services update SERVICE_NAME \
  --update-env-vars KEY=NEW_VALUE \
  --region REGION

# 刪除環境變數
gcloud run services update SERVICE_NAME \
  --remove-env-vars KEY \
  --region REGION
```

