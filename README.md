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

## Vercel 部署

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

### 替代方案

如果需要完整功能（包括 Selenium），建議使用：
- **Heroku** - 支援完整 Python 環境
- **Railway** - 支援 Docker 和完整依賴
- **Render** - 免費 Python 應用託管
- **DigitalOcean App Platform** - 支援完整功能

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
