# 修復記憶體不足問題

## 問題

錯誤：`Memory limit of 512 MiB exceeded with 516 MiB used`

Playwright 和瀏覽器需要較多記憶體，預設的 512 MiB 不足。

## 解決方案

### 方法一：使用命令列更新（推薦）

```bash
gcloud run services update professor-crawler \
  --memory 2Gi \
  --cpu 2 \
  --region asia-east1
```

### 方法二：在 Cloud Console 中更新

1. 訪問 Google Cloud Console
2. 進入 Cloud Run 服務頁面
3. 選擇 `professor-crawler` 服務
4. 點擊「編輯和部署新版本」
5. 在「資源配置」區塊：
   - 將「記憶體」改為 **2 GiB**
   - 將「CPU」改為 **2**
6. 點擊「部署」

### 方法三：重新部署時指定

```bash
gcloud run deploy professor-crawler \
  --image gcr.io/YOUR_PROJECT_ID/professor-crawler:latest \
  --region asia-east1 \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --allow-unauthenticated
```

## 驗證配置

檢查當前配置：

```bash
gcloud run services describe professor-crawler \
  --region asia-east1 \
  --format="value(spec.template.spec.containers[0].resources.limits)"
```

應該顯示：
```
memory: 2Gi
cpu: 2
```

## 如果 2Gi 仍然不足

可以增加到 4Gi：

```bash
gcloud run services update professor-crawler \
  --memory 4Gi \
  --cpu 2 \
  --region asia-east1
```

## 成本影響

- **2Gi 記憶體**: 每 GB 小時約 $0.00000250
- **4Gi 記憶體**: 每 GB 小時約 $0.00000250（按使用量計費）

記憶體增加會增加成本，但對於 Playwright 是必要的。

