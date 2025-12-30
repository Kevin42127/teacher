# Playwright 瀏覽器問題完整解決方案

## 問題

錯誤：`Executable doesn't exist at /usr/local/lib/python3.11/site-packages/playwright/driver/package/.local-browsers/chromium-1200/chrome-linux64/chrome`

## 解決方案

### 方案一：確保瀏覽器正確安裝（已更新）

Dockerfile 已更新，包含：
1. 正確的 Playwright 安裝順序
2. 瀏覽器驗證步驟
3. 系統依賴安裝

### 方案二：使用 Playwright 官方 Docker 映像

如果方案一仍有問題，可以使用 Playwright 官方映像：

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 300 app:app
```

### 方案三：手動指定瀏覽器路徑

在代碼中明確指定瀏覽器路徑：

```python
from crawl4ai import AsyncWebCrawler
import os

# 設置瀏覽器路徑
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'

crawler = AsyncWebCrawler(
    headless=True,
    verbose=False,
    browser_type="chromium"
)
```

### 方案四：使用替代爬蟲方案

如果 Playwright 持續有問題，可以考慮使用：

1. **httpx + BeautifulSoup**（靜態內容）
2. **Selenium**（需要額外配置）
3. **外部爬蟲服務**（ScraperAPI、Bright Data）

## 驗證步驟

### 本地測試 Docker 映像

```bash
# 建置
docker build -t professor-crawler .

# 測試 Playwright
docker run --rm professor-crawler python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); browser = p.chromium.launch(headless=True); print('OK'); browser.close(); p.stop()"
```

### 檢查瀏覽器路徑

```bash
docker run --rm professor-crawler python -c "from playwright.sync_api import sync_playwright; import os; print('BROWSERS_PATH:', os.environ.get('PLAYWRIGHT_BROWSERS_PATH')); p = sync_playwright().start(); browser = p.chromium.launch(headless=True); print('Executable:', browser.executable_path)"
```

## 重新部署

```bash
# 重新建置
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/professor-crawler

# 部署
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --region asia-east1 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300
```

## 如果問題持續

1. **檢查日誌**：
```bash
gcloud run services logs read professor-crawler --region asia-east1 --limit 100
```

2. **增加記憶體**：
```bash
gcloud run services update professor-crawler \
  --memory 4Gi \
  --region asia-east1
```

3. **考慮使用 Playwright 官方映像**（方案二）

