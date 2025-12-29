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

## Heroku 部署（推薦 - 支援完整功能）

### 部署步驟

1. **安裝 Heroku CLI**
   - 下載：https://devcenter.heroku.com/articles/heroku-cli
   - 或使用：`npm install -g heroku`

2. **登入 Heroku**
```bash
heroku login
```

3. **創建 Heroku 應用**
```bash
heroku create your-app-name
```

4. **設置 Buildpacks**
```bash
heroku buildpacks:add heroku/python
heroku buildpacks:add heroku/google-chrome
```

5. **部署到 Heroku**
```bash
git push heroku main
```

6. **開啟應用**
```bash
heroku open
```

### 或使用 GitHub 自動部署

1. 在 [Heroku Dashboard](https://dashboard.heroku.com/apps) 創建新應用
2. 在 Settings → Deploy 中連接 GitHub 倉庫
3. 啟用自動部署（Automatic deploys）
4. 點擊 "Deploy Branch" 手動部署

### Heroku 優勢

✅ **完整功能支援**：
- ✅ 支援 Selenium 和 Chrome
- ✅ 支援深度爬蟲功能
- ✅ 完整 Python 環境
- ✅ 免費方案可用

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
