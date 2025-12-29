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

## Fly.io 部署（推薦 - 支援完整功能）

### 部署步驟

1. **安裝 Fly CLI**
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# 或使用其他安裝方式
# https://fly.io/docs/hands-on/install-flyctl/
```

2. **登入 Fly.io**
```bash
fly auth login
```

3. **初始化應用**
```bash
fly launch
```
   - 會自動偵測 Dockerfile
   - 輸入應用名稱（或使用預設）
   - 選擇區域（建議選擇 `hkg` 或 `nrt` 亞洲區域）

4. **部署**
```bash
fly deploy
```

5. **查看應用**
```bash
fly open
```

### Fly.io 優勢

✅ **完整功能支援**：
- ✅ 支援 Selenium 和 Chrome（已配置）
- ✅ 支援深度爬蟲功能
- ✅ 完整 Python 環境
- ✅ 免費額度（3 個共享 CPU 應用）
- ✅ 全球邊緣部署
- ✅ 自動 HTTPS
- ✅ 自動擴展
- ✅ 無需信用卡即可開始

### 價格

- **免費額度**: 3 個共享 CPU 應用
- **按使用量計費**: 超出免費額度後才收費
- **預估**: 輕量使用可能完全免費

### 配置說明

專案已包含：
- `Dockerfile` - 自動安裝 Chrome 和依賴
- `fly.toml` - Fly.io 配置文件
- 所有深度爬蟲功能已就緒

### 常用命令

```bash
# 查看應用狀態
fly status

# 查看日誌
fly logs

# 重啟應用
fly restart

# 查看應用資訊
fly info
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
