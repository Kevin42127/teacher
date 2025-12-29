import csv
import json
from typing import List, Dict
from datetime import datetime
import pandas as pd


class DataExporter:
    @staticmethod
    def to_csv(data: List[Dict[str, str]], filename: str = None) -> str:
        if not filename:
            filename = f"professors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        if not data:
            return None
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        return filename
    
    @staticmethod
    def to_json(data: List[Dict[str, str]], filename: str = None) -> str:
        if not filename:
            filename = f"professors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filename
    
    @staticmethod
    def to_csv_string(data: List[Dict[str, str]]) -> str:
        if not data:
            return ""
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False, encoding='utf-8-sig')
    
    @staticmethod
    def to_json_string(data: List[Dict[str, str]]) -> str:
        return json.dumps(data, ensure_ascii=False, indent=2)

