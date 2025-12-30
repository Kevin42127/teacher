from http.server import BaseHTTPRequestHandler
import json
import io
import csv
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            professors = data.get('data', [])
            
            if not professors:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': '沒有資料可匯出'}).encode())
                return
            
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=['name', 'email', 'department'])
            writer.writeheader()
            for prof in professors:
                writer.writerow(prof)
            
            csv_content = output.getvalue()
            csv_bytes = csv_content.encode('utf-8-sig')
            csv_base64 = base64.b64encode(csv_bytes).decode('utf-8')
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': True,
                'data': csv_base64,
                'filename': 'professors.csv'
            }).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({
                'success': False,
                'error': str(e)
            }).encode())

