# 大學教授資訊採集機器人

使用 Crawl4AI 從大學網站上自動提取教授的姓名、電子郵件和科系資訊，並匯出為 CSV 或 JSON 格式。

## 功能特色

- 自動爬取大學網站並提取教授資訊
- 支援提取姓名、電子郵件、科系等欄位
- 匯出為 CSV 或 JSON 格式
- 支援臺灣及其他國家的大學網站
- 使用 AI 模型智能解析網頁內容

## 安裝步驟

### 1. 安裝 Python 依賴

```bash
pip install -r requirements.txt
```

### 2. 安裝 Playwright 瀏覽器

```bash
playwright install
```

### 3. 設定 AI 模型 API Key

建立 `.env` 檔案並加入對應的 API Key（根據您選擇的模型）：

```
# OpenAI 模型
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Claude 模型
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Google Gemini 模型
GOOGLE_API_KEY=your_google_api_key_here

# Groq AI 模型
GROQ_API_KEY=your_groq_api_key_here
```

**支援的模型：**
- **OpenAI**: GPT-4o Mini, GPT-4, GPT-3.5 Turbo
- **Anthropic**: Claude 3 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **Google**: Gemini Pro, Gemini 1.5 Pro, Gemini 1.5 Flash
- **Groq**: Llama 3.1 70B Versatile, Llama 3.1 8B Instant, Mixtral 8x7B, Gemma 7B IT

在網頁介面中也可以直接輸入 API Key，或使用命令列參數 `--api-key`。

## 使用方法

### 網頁介面（推薦）

1. 啟動後端伺服器：

```bash
python app.py
```

2. 開啟瀏覽器訪問：

```
http://localhost:5000
```

3. 在網頁介面中輸入大學網站網址，點擊「開始採集」按鈕

4. 採集完成後，可以點擊「匯出 Excel」按鈕下載 CSV 檔案

### 命令列介面

#### 基本用法

```bash
python professor_crawler.py <大學網站URL>
```

### 指定輸出格式

```bash
# 只匯出 JSON
python professor_crawler.py <URL> --format json

# 只匯出 CSV
python professor_crawler.py <URL> --format csv

# 同時匯出兩種格式（預設）
python professor_crawler.py <URL> --format both
```

### 指定輸出檔名

```bash
python professor_crawler.py <URL> --output my_professors
```

### 使用 API Key 和模型參數

```bash
# 使用自訂 API Key
python professor_crawler.py <URL> --api-key your_api_key

# 指定不同的 AI 模型
python professor_crawler.py <URL> --provider anthropic/claude-3-sonnet
python professor_crawler.py <URL> --provider google/gemini-pro
```

## 使用範例

```bash
# 爬取臺灣大學教授資訊
python professor_crawler.py https://www.ntu.edu.tw/faculty

# 指定輸出檔名和格式
python professor_crawler.py https://www.nthu.edu.tw/faculty --output nthu_professors --format json
```

## 輸出格式

### JSON 格式

```json
[
  {
    "name": "王小明",
    "email": "wang@university.edu.tw",
    "department": "資訊工程學系"
  },
  {
    "name": "李美麗",
    "email": "lee@university.edu.tw",
    "department": "電機工程學系"
  }
]
```

### CSV 格式

```csv
name,email,department
王小明,wang@university.edu.tw,資訊工程學系
李美麗,lee@university.edu.tw,電機工程學系
```

## 注意事項

- 請確保遵守目標網站的 robots.txt 和使用條款
- 某些網站可能有反爬蟲機制，可能需要調整爬取策略
- 需要有效的 AI 模型 API Key 才能使用（OpenAI、Anthropic 或 Google）
- 建議在爬取前先確認目標網站的結構和內容格式
- 不同模型的成本和效能可能不同，請根據需求選擇合適的模型

## 技術架構

### 後端
- **Flask**: Web 框架
- **Crawl4AI**: 網頁爬取框架
- **Playwright**: 瀏覽器自動化
- **OpenAI GPT-4o-mini**: AI 內容提取
- **Pydantic**: 資料驗證和模型定義

### 前端
- **HTML/CSS/JavaScript**: 現代化網頁介面
- **Google Material Icons**: 圖標系統
- **響應式設計**: 支援各種螢幕尺寸

