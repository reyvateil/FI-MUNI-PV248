import http.server

class http_handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200, 'OK')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'<h1>You asked for ')
        self.wfile.write(bytes(source=self.path[1:], encoding='utf8'))
        self.wfile.write(b'</h1>')
        self.wfile.write(b'Your activity is monitored: ')
        self.wfile.write(bytes("{}:{}".format(self.client_address[0], self.client_address[1]), encoding='utf8'))


def run(server_class=http.server.HTTPServer, handler_class=http_handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()