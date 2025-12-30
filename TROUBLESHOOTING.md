# 故障排除指南

## 無法採集的常見問題

### 1. 環境變數未正確設置

#### 檢查環境變數

```bash
# 檢查 Cloud Run 服務的環境變數
gcloud run services describe professor-crawler \
  --region asia-east1 \
  --format="value(spec.template.spec.containers[0].env)"
```

#### 解決方法

1. **確認環境變數名稱正確**
   - 必須是 `GROQ_API_KEY`（大小寫敏感）
   - 不要有多餘的空格

2. **重新部署服務**
   ```bash
   gcloud run services update professor-crawler \
     --set-env-vars GROQ_API_KEY=your_key \
     --region asia-east1
   ```

3. **檢查服務日誌**
   ```bash
   gcloud run services logs read professor-crawler \
     --region asia-east1 \
     --limit 50
   ```

### 2. Playwright 相關問題

#### 症狀
- 錯誤訊息包含 "playwright" 或 "browser"
- 連接被重置
- 超時錯誤

#### 解決方法

1. **增加記憶體和 CPU**
   ```bash
   gcloud run services update professor-crawler \
     --memory 4Gi \
     --cpu 2 \
     --region asia-east1
   ```

2. **檢查 Dockerfile 中的 Playwright 安裝**
   - 確認已安裝 Chromium
   - 確認系統依賴已安裝

3. **增加超時時間**
   ```bash
   gcloud run services update professor-crawler \
     --timeout 600 \
     --region asia-east1
   ```

### 3. API Key 無效

#### 檢查 API Key

```python
# 在本地測試
from groq import Groq
client = Groq(api_key="your_key")
# 如果 API Key 無效會拋出錯誤
```

#### 解決方法

1. **確認 API Key 格式正確**
   - Groq API Key 通常以 `gsk_` 開頭
   - 確認沒有多餘的空格或換行

2. **測試 API Key**
   ```bash
   curl https://api.groq.com/openai/v1/models \
     -H "Authorization: Bearer your_groq_api_key"
   ```

### 4. 網路連接問題

#### 症狀
- `ERR_CONNECTION_RESET`
- `Timeout`
- `Network error`

#### 解決方法

1. **檢查目標網站是否可訪問**
   - 在瀏覽器中測試網址
   - 確認網站沒有封鎖 Cloud Run 的 IP

2. **增加重試機制**
   - 系統已包含基本錯誤處理
   - 可以考慮添加重試邏輯

### 5. 記憶體不足

#### 症狀
- 服務崩潰
- 超時錯誤
- 日誌顯示 OOM (Out of Memory)

#### 解決方法

```bash
# 增加記憶體
gcloud run services update professor-crawler \
  --memory 4Gi \
  --region asia-east1
```

### 6. 超時問題

#### 症狀
- 請求在 300 秒內未完成
- 返回 504 Gateway Timeout

#### 解決方法

```bash
# 增加超時時間
gcloud run services update professor-crawler \
  --timeout 600 \
  --region asia-east1
```

## 調試步驟

### 1. 查看服務日誌

```bash
# 即時查看日誌
gcloud run services logs tail professor-crawler \
  --region asia-east1

# 查看最近的日誌
gcloud run services logs read professor-crawler \
  --region asia-east1 \
  --limit 100
```

### 2. 本地測試

```bash
# 使用 Docker 本地測試
docker build -t professor-crawler .
docker run -p 8080:8080 \
  -e GROQ_API_KEY=your_key \
  -e PORT=8080 \
  professor-crawler

# 測試 API
curl -X POST http://localhost:8080/api/crawl \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```

### 3. 檢查環境變數

在應用程式中添加調試端點：

```python
@app.route('/api/debug/env', methods=['GET'])
def debug_env():
    return jsonify({
        'GROQ_API_KEY_set': bool(os.getenv('GROQ_API_KEY')),
        'GROQ_API_KEY_length': len(os.getenv('GROQ_API_KEY', ''))
    })
```

## 常見錯誤訊息

### "需要提供 Groq API Key"
- **原因**: 環境變數未設置
- **解決**: 在 Cloud Run 中設置 `GROQ_API_KEY`

### "連接被重置"
- **原因**: 網站有反爬蟲機制或網路問題
- **解決**: 嘗試其他網站或增加重試

### "網頁內容為空"
- **原因**: 爬取失敗或網站結構特殊
- **解決**: 檢查網址是否正確，查看日誌

### "JSON 解析錯誤"
- **原因**: Groq API 返回的格式不符合預期
- **解決**: 檢查 API Key 是否有效，查看完整錯誤訊息

## 驗證清單

在報告問題前，請確認：

- [ ] 環境變數已正確設置
- [ ] API Key 格式正確且有效
- [ ] 服務已重新部署
- [ ] 記憶體和 CPU 配置足夠
- [ ] 超時時間足夠長
- [ ] 目標網站可以正常訪問
- [ ] 已查看服務日誌

## 獲取幫助

如果問題持續存在：

1. **收集日誌**
   ```bash
   gcloud run services logs read professor-crawler \
     --region asia-east1 \
     --limit 200 > logs.txt
   ```

2. **檢查服務狀態**
   ```bash
   gcloud run services describe professor-crawler \
     --region asia-east1
   ```

3. **測試 API Key**
   - 確認 API Key 在本地可以正常使用
   - 確認 API Key 沒有過期

