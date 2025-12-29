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

## Railway 部署（推薦 - 支援完整功能）

### 部署步驟

1. **註冊 Railway 帳號**
   - 訪問：https://railway.app
   - 使用 GitHub 帳號登入

2. **創建新專案**
   - 在 Dashboard 點擊 "New Project"
   - 選擇 "Deploy from GitHub repo"
   - 選擇倉庫：`Kevin42127/collection`

3. **自動部署**
   - Railway 會自動偵測 Python 專案
   - 自動使用 Dockerfile 構建
   - 自動安裝 Chrome 和依賴
   - 自動設置環境變數

4. **環境變數**（自動設置，無需手動配置）
   - `PORT`: Railway 自動設置
   - `CHROMIUM_PATH`: `/usr/bin/chromium`
   - `CHROMEDRIVER_PATH`: `/usr/bin/chromedriver`

5. **查看部署**
   - 在 Dashboard 查看構建日誌
   - 部署完成後會顯示訪問 URL

### Railway 優勢

✅ **完整功能支援**：
- ✅ 支援 Selenium 和 Chrome（已配置）
- ✅ 支援深度爬蟲功能
- ✅ 完整 Python 環境
- ✅ 免費額度 $5/月
- ✅ 自動 HTTPS
- ✅ 自動部署（GitHub push 觸發）
- ✅ 無需信用卡即可開始

### 價格

- **免費額度**: $5/月
- **按使用量計費**: 超出額度後才收費
- **預估**: 輕量使用可能完全免費

### 配置說明

專案已包含：
- `Dockerfile` - 自動安裝 Chrome 和依賴
- `railway.json` - Railway 配置文件
- 所有深度爬蟲功能已就緒

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
