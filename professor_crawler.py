import os
import json
import csv
import argparse
import re
from typing import List, Optional
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler
from groq import Groq
import asyncio

load_dotenv()

class ProfessorInfo(BaseModel):
    name: str = Field(..., description="教授姓名")
    email: str = Field(..., description="教授的電子郵件地址")
    department: str = Field(..., description="教授所屬的科系")

class ProfessorCrawler:
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        self.model = model
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        
        if not self.api_key:
            raise ValueError("需要提供 Groq API Key，請設定環境變數 GROQ_API_KEY 或使用 --api-key 參數")
        
        self.client = Groq(api_key=self.api_key)
        self.crawler = AsyncWebCrawler(
            headless=True,
            verbose=False
        )
    
    def _extract_with_groq(self, content: str) -> List[ProfessorInfo]:
        prompt = f"""請從以下網頁內容中提取教授的資訊。請只提取 4 位教授的資訊。

要求：
1. 只提取 4 位教授的資訊，不要超過 4 位
2. 每個教授包含三個欄位：name（姓名）、email（電子郵件）、department（科系）
3. 如果某個欄位找不到，請使用空字串 ""
4. 請以 JSON 陣列格式返回，只包含 4 個物件

網頁內容：
{content[:20000]}

請返回 JSON 陣列，只包含 4 位教授的資訊，格式如下：
[
  {{"name": "姓名1", "email": "email1@example.com", "department": "科系名稱1"}},
  {{"name": "姓名2", "email": "email2@example.com", "department": "科系名稱2"}},
  {{"name": "姓名3", "email": "email3@example.com", "department": "科系名稱3"}},
  {{"name": "姓名4", "email": "email4@example.com", "department": "科系名稱4"}}
]

重要：只返回 4 位教授的資訊，不要超過 4 位。只返回 JSON 陣列，不要有其他文字說明。"""

        response_text = ""
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_completion_tokens=8192,
                top_p=1,
                stream=False,
                stop=None
            )
            
            response_text = completion.choices[0].message.content.strip()
            
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            data = json.loads(response_text)
            
            professors = []
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        try:
                            professor = ProfessorInfo(**item)
                            professors.append(professor)
                            if len(professors) >= 4:
                                break
                        except Exception as e:
                            print(f"解析資料時發生錯誤: {e}, 資料: {item}")
                            continue
            elif isinstance(data, dict):
                try:
                    professor = ProfessorInfo(**data)
                    professors.append(professor)
                except Exception as e:
                    print(f"解析資料時發生錯誤: {e}")
            
            return professors[:4]
            
        except json.JSONDecodeError as e:
            print(f"JSON 解析錯誤: {e}")
            if response_text:
                print(f"回應內容: {response_text[:500]}")
            return []
        except Exception as e:
            print(f"Groq API 調用錯誤: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    async def _crawl_async(self, url: str) -> List[ProfessorInfo]:
        print(f"正在爬取: {url}")
        
        try:
            result = await self.crawler.arun(url=url)
            
            if not result.markdown and not result.html:
                print("警告: 未獲取到網頁內容")
                return []
            
            content = result.markdown or result.html
            
            if not content:
                print("警告: 網頁內容為空")
                return []
            
            print(f"網頁內容長度: {len(content)} 字元")
            print("正在使用 Groq AI 提取教授資訊（限制 4 位）...")
            
            professors = self._extract_with_groq(content)
            
            print(f"成功提取 {len(professors)} 位教授的資訊")
            return professors
            
        except Exception as e:
            print(f"爬取過程中發生錯誤: {e}")
            import traceback
            traceback.print_exc()
            return []
    
    def crawl(self, url: str) -> List[ProfessorInfo]:
        return asyncio.run(self._crawl_async(url))
    
    def export_to_json(self, professors: List[ProfessorInfo], output_path: str):
        data = [prof.model_dump() for prof in professors]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"已匯出 {len(professors)} 筆資料到 {output_path}")
    
    def export_to_csv(self, professors: List[ProfessorInfo], output_path: str):
        if not professors:
            print("沒有資料可匯出")
            return
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'email', 'department'])
            writer.writeheader()
            for prof in professors:
                writer.writerow(prof.model_dump())
        print(f"已匯出 {len(professors)} 筆資料到 {output_path}")

def main():
    parser = argparse.ArgumentParser(description='大學教授資訊採集機器人')
    parser.add_argument('url', help='要爬取的大學網站 URL')
    parser.add_argument('--api-key', help='Groq API Key (可選，也可使用環境變數 GROQ_API_KEY)')
    parser.add_argument('--model', '-m', default='llama-3.3-70b-versatile',
                       help='Groq 模型名稱 (預設: llama-3.3-70b-versatile)')
    parser.add_argument('--output', '-o', default='professors', help='輸出檔案名稱 (不含副檔名)')
    parser.add_argument('--format', '-f', choices=['json', 'csv', 'both'], default='both', 
                       help='輸出格式: json, csv, 或 both (預設: both)')
    
    args = parser.parse_args()
    
    try:
        crawler = ProfessorCrawler(api_key=args.api_key, model=args.model)
        professors = crawler.crawl(args.url)
        
        if not professors:
            print("未找到任何教授資訊")
            return
        
        if args.format in ['json', 'both']:
            crawler.export_to_json(professors, f"{args.output}.json")
        
        if args.format in ['csv', 'both']:
            crawler.export_to_csv(professors, f"{args.output}.csv")
        
    except Exception as e:
        print(f"執行錯誤: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())

