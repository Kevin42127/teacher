#!/bin/bash
# 更新 Cloud Run 服務的記憶體配置

gcloud run services update professor-crawler \
  --memory 2Gi \
  --cpu 2 \
  --region asia-east1

