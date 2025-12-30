# 如何判斷網站是否有反爬蟲機制

## 快速檢測方法

### 1. 瀏覽器檢查

#### 檢查 Cloudflare
- 打開網站後，查看頁面原始碼（F12）
- 搜尋 "cloudflare" 或 "cf-"
- 如果看到 Cloudflare 相關的 JavaScript 或標記，表示有 Cloudflare 保護

#### 檢查 CAPTCHA
- 訪問網站時出現驗證碼
- 需要完成 reCAPTCHA 或 hCaptcha
- 表示有反爬蟲機制

### 2. 網路請求檢查

#### 使用瀏覽器開發者工具
1. 按 F12 打開開發者工具
2. 切換到「Network」標籤
3. 重新載入頁面
4. 檢查請求標頭和回應

#### 檢查項目：
- **Status Code**: 如果返回 403 Forbidden，可能有反爬蟲
- **Response Headers**: 檢查是否有 `cf-ray`（Cloudflare）或 `x-protected-by` 等標記
- **Request Headers**: 檢查 User-Agent 是否被檢查

### 3. 程式碼檢測

#### 檢查 robots.txt
```
訪問：https://網站網址/robots.txt
```
- 如果明確禁止爬蟲，表示有防護意識
- 但 robots.txt 只是建議，不是強制

#### 檢查 JavaScript 驗證
- 查看頁面原始碼
- 搜尋 "bot"、"crawler"、"spider"
- 如果有相關檢測代碼，可能有反爬蟲

## 常見反爬蟲特徵

### 1. Cloudflare 保護
**特徵：**
- 頁面載入前出現「正在檢查您的瀏覽器」訊息
- 需要等待幾秒才能訪問
- 網址包含 `__cf_bm` 參數

**檢測方法：**
```javascript
// 在瀏覽器控制台執行
console.log(document.cookie.includes('__cf'));
```

### 2. Rate Limiting
**特徵：**
- 短時間內多次訪問後被限制
- 返回 429 Too Many Requests
- 需要等待一段時間才能繼續

**檢測方法：**
- 快速重新載入頁面多次
- 觀察是否出現限制訊息

### 3. User-Agent 檢測
**特徵：**
- 使用 curl 或 wget 無法訪問
- 但瀏覽器可以正常訪問
- 返回 403 Forbidden

**檢測方法：**
```bash
# 測試不同 User-Agent
curl -A "Mozilla/5.0" https://網站網址
curl -A "python-requests" https://網站網址
```

### 4. JavaScript 驗證
**特徵：**
- 頁面內容需要 JavaScript 才能顯示
- 禁用 JavaScript 後頁面空白
- 使用 SPA（單頁應用）架構

**檢測方法：**
- 在瀏覽器中禁用 JavaScript
- 重新載入頁面
- 如果內容消失，表示需要 JavaScript

### 5. IP 封鎖
**特徵：**
- 特定 IP 無法訪問
- 返回 403 或連接被拒絕
- 其他 IP 可以正常訪問

**檢測方法：**
- 使用不同網路環境測試
- 使用 VPN 或代理測試

## 實用檢測工具

### 1. 瀏覽器擴充功能
- **Wappalyzer**: 檢測網站使用的技術
- **BuiltWith**: 分析網站架構
- **WhatRuns**: 識別網站技術堆疊

### 2. 線上工具
- **SecurityHeaders.com**: 檢查安全標頭
- **SSL Labs**: 檢查 SSL/TLS 配置
- **PageSpeed Insights**: 分析網站效能和技術

### 3. 命令列工具
```bash
# 檢查 HTTP 標頭
curl -I https://網站網址

# 檢查完整回應
curl -v https://網站網址

# 檢查是否被重定向
curl -L https://網站網址
```

## 系統檢測方法

### 使用我們的系統測試
1. 在系統中輸入網址
2. 觀察錯誤訊息：
   - "未獲取到網頁內容" → 可能有反爬蟲
   - "網頁內容為空" → 可能需要 JavaScript
   - 長時間無回應 → 可能被限制

### 檢查日誌
查看後端日誌輸出：
- 如果出現 "403"、"429" 等錯誤碼
- 如果出現 "blocked"、"forbidden" 等關鍵字
- 表示可能有反爬蟲機制

## 應對策略

### 如果檢測到反爬蟲：

1. **使用 Playwright（已支援）**
   - 系統已使用 Playwright 模擬真實瀏覽器
   - 可以執行 JavaScript
   - 降低被檢測機率

2. **調整請求頻率**
   - 不要過於頻繁請求
   - 在請求之間加入延遲
   - 模擬人類行為

3. **使用代理**
   - 輪換 IP 位址
   - 避免單一 IP 過多請求

4. **遵守規則**
   - 檢查 robots.txt
   - 遵守網站使用條款
   - 不要過度爬取

## 快速判斷流程圖

```
訪問網站
  ↓
是否出現驗證碼？
  ├─ 是 → 有反爬蟲（CAPTCHA）
  └─ 否 → 繼續檢查
      ↓
是否出現「檢查瀏覽器」？
  ├─ 是 → 有反爬蟲（Cloudflare）
  └─ 否 → 繼續檢查
      ↓
使用 curl 測試
  ├─ 返回 403 → 有反爬蟲（User-Agent 檢測）
  └─ 正常 → 繼續檢查
      ↓
禁用 JavaScript 測試
  ├─ 內容消失 → 需要 JavaScript（可能無反爬蟲）
  └─ 內容正常 → 可能無反爬蟲
```

