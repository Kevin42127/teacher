import os
import json
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from professor_crawler import ProfessorCrawler
import io
import csv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/api/models', methods=['GET'])
def get_models():
    models = [
        {'value': 'openai/gpt-4o-mini', 'label': 'OpenAI GPT-4o Mini', 'env': 'OPENAI_API_KEY'},
        {'value': 'openai/gpt-4', 'label': 'OpenAI GPT-4', 'env': 'OPENAI_API_KEY'},
        {'value': 'openai/gpt-3.5-turbo', 'label': 'OpenAI GPT-3.5 Turbo', 'env': 'OPENAI_API_KEY'},
        {'value': 'anthropic/claude-3-sonnet', 'label': 'Anthropic Claude 3 Sonnet', 'env': 'ANTHROPIC_API_KEY'},
        {'value': 'anthropic/claude-3-opus', 'label': 'Anthropic Claude 3 Opus', 'env': 'ANTHROPIC_API_KEY'},
        {'value': 'anthropic/claude-3-haiku', 'label': 'Anthropic Claude 3 Haiku', 'env': 'ANTHROPIC_API_KEY'},
        {'value': 'google/gemini-pro', 'label': 'Google Gemini Pro', 'env': 'GOOGLE_API_KEY'},
        {'value': 'google/gemini-1.5-pro', 'label': 'Google Gemini 1.5 Pro', 'env': 'GOOGLE_API_KEY'},
        {'value': 'google/gemini-1.5-flash', 'label': 'Google Gemini 1.5 Flash', 'env': 'GOOGLE_API_KEY'},
        {'value': 'groq/llama-3.1-70b-versatile', 'label': 'Groq Llama 3.1 70B Versatile', 'env': 'GROQ_API_KEY'},
        {'value': 'groq/llama-3.1-8b-instant', 'label': 'Groq Llama 3.1 8B Instant', 'env': 'GROQ_API_KEY'},
        {'value': 'groq/mixtral-8x7b-32768', 'label': 'Groq Mixtral 8x7B', 'env': 'GROQ_API_KEY'},
        {'value': 'groq/gemma-7b-it', 'label': 'Groq Gemma 7B IT', 'env': 'GROQ_API_KEY'},
    ]
    return jsonify({'models': models})

@app.route('/api/crawl', methods=['POST'])
def crawl():
    try:
        data = request.json
        url = data.get('url')
        model = data.get('model', 'llama-3.3-70b-versatile')
        api_key = data.get('api_key', None)
        
        if not url:
            return jsonify({'error': '請提供網址'}), 400
        
        crawler = ProfessorCrawler(api_key=api_key, model=model)
        professors = crawler.crawl(url)
        
        result = [prof.model_dump() for prof in professors]
        
        return jsonify({
            'success': True,
            'data': result,
            'count': len(result)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export/excel', methods=['POST'])
def export_excel():
    try:
        data = request.json
        professors = data.get('data', [])
        
        if not professors:
            return jsonify({'error': '沒有資料可匯出'}), 400
        
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=['name', 'email', 'department'])
        writer.writeheader()
        for prof in professors:
            writer.writerow(prof)
        
        output.seek(0)
        
        return send_file(
            io.BytesIO(output.getvalue().encode('utf-8-sig')),
            mimetype='text/csv',
            as_attachment=True,
            download_name='professors.csv'
        )
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/')
def index():
    from flask import send_from_directory
    import os
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)

