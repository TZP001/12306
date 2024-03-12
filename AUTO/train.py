from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

# 用于存储token、je和uk的字典
data = {}

class APIServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if parsed_url.path == '/set_tk':
            token = query_params.get('tk', [''])[0]
            data['tk'] = token
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("TK set successfully", 'utf-8'))

        elif parsed_url.path == '/set_je':
            je = query_params.get('je', [''])[0]
            data['je'] = je
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("JE set successfully", 'utf-8'))

        elif parsed_url.path == '/set_uk':
            uk = query_params.get('uk', [''])[0]
            data['uk'] = uk
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("UK set successfully", 'utf-8'))

        elif parsed_url.path == '/get_tk':
            token = data.get('token', '')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(token, 'utf-8'))

        elif parsed_url.path == '/get_je':
            je = data.get('je', '')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(je, 'utf-8'))

        elif parsed_url.path == '/get_uk':
            uk = data.get('uk', '')
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes(uk, 'utf-8'))

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(bytes("Not found", 'utf-8'))

def run_server():
    server_address = ('', 5000)
    httpd = HTTPServer(server_address, APIServer)
    print('Starting server on 5000...')
    httpd.serve_forever()

run_server()
