# 修復 Playwright 瀏覽器問題

## 問題描述

錯誤訊息：`Executable doesn't exist at /ms-playwright/chromium-1200/chrome-linux64/chrome`

這表示 Playwright 無法找到 Chromium 瀏覽器可執行檔。

## 解決方案

### 1. 確保 Dockerfile 正確安裝瀏覽器

已更新 Dockerfile 使用：
```dockerfile
RUN playwright install chromium
RUN playwright install-deps chromium
```

### 2. 設置環境變數

在 Cloud Run 中設置以下環境變數：

```bash
PLAYWRIGHT_BROWSERS_PATH=0
PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=0
```

### 3. 驗證安裝

在本地測試 Docker 映像：

```bash
# 建置映像
docker build -t professor-crawler .

# 執行並檢查 Playwright
docker run --rm professor-crawler python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); print('Playwright OK')"
```

### 4. 替代方案：使用系統 Chromium

如果 Playwright 安裝仍有問題，可以修改代碼使用系統 Chromium：

```python
from crawl4ai import AsyncWebCrawler

crawler = AsyncWebCrawler(
    headless=True,
    browser_type="chromium",
    verbose=False
)
```

### 5. 檢查瀏覽器路徑

在代碼中添加調試資訊：

```python
import os
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    print(f"Browser path: {browser.executable_path}")
```

## 重新部署

修正後重新建置和部署：

```bash
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/professor-crawler
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler \
  --region asia-east1 \
  --set-env-vars PLAYWRIGHT_BROWSERS_PATH=0
```

