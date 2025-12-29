from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from scraper import ProfessorScraper
from exporter import DataExporter
import os
from datetime import datetime
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        export_format = data.get('format', 'csv').lower()
        
        if not url:
            return jsonify({'error': '請提供有效的 URL'}), 400
        
        scraper = ProfessorScraper()
        professors = scraper.scrape(url)
        
        if not professors:
            return jsonify({'error': '未找到教授資料，請檢查網址或嘗試其他頁面'}), 404
        
        return jsonify({
            'success': True,
            'data': professors,
            'count': len(professors)
        })
    
    except Exception as e:
        return jsonify({'error': f'處理失敗: {str(e)}'}), 500

@app.route('/api/export', methods=['POST'])
def export():
    try:
        data = request.get_json()
        professors = data.get('data', [])
        export_format = data.get('format', 'csv').lower()
        
        if not professors:
            return jsonify({'error': '沒有資料可匯出'}), 400
        
        exporter = DataExporter()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if export_format == 'csv':
            csv_data = exporter.to_csv_string(professors)
            output = io.BytesIO()
            output.write(csv_data.encode('utf-8-sig'))
            output.seek(0)
            
            return send_file(
                output,
                mimetype='text/csv',
                as_attachment=True,
                download_name=f'professors_{timestamp}.csv'
            )
        
        elif export_format == 'json':
            json_data = exporter.to_json_string(professors)
            output = io.BytesIO()
            output.write(json_data.encode('utf-8'))
            output.seek(0)
            
            return send_file(
                output,
                mimetype='application/json',
                as_attachment=True,
                download_name=f'professors_{timestamp}.json'
            )
        
        else:
            return jsonify({'error': '不支援的匯出格式'}), 400
    
    except Exception as e:
        return jsonify({'error': f'匯出失敗: {str(e)}'}), 500

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

