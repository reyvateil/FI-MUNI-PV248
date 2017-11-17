import http.server
from pprint import pprint
import urllib.parse as up
import search
import json

class http_handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        url_parsed = up.urlparse(self.path)
        query_string = url_parsed.query
        path_string = url_parsed.path
        query_map = up.parse_qs(query_string)
        if '/result' == path_string and 'f' in query_map and 'q' in query_map:
            query_string = query_map['q'][0].lower()
            if query_map['f'][0] == 'json':
                self.send_response(200, 'OK')
                self.send_header('Content-type', 'text/json')
                self.end_headers()
                result = search.get_composers_and_scores_by_name("%{}%".format(query_string))
                self.wfile.write(bytes(json.dumps(result, ensure_ascii=False), encoding='utf8'))
            elif query_map['f'][0] == 'html':
                self.send_response(200, 'OK')
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                result = search.get_composers_and_scores_by_name("%{}%".format(query_string))
                json_dict = json.loads(json.dumps(result, ensure_ascii=False))
                self.wfile.write(bytes('<h1>Results for query \'{}\''.format(query_string), encoding='utf8'))
                for composer in json_dict:
                    self.wfile.write(bytes('<h2>{}</h2>'.format(composer), encoding='utf8'))
                    self.wfile.write(bytes('<ul>', encoding='utf8'))
                    for score in json_dict[composer]:
                        self.wfile.write(bytes('<li>{}</li>'.format(score), encoding='utf8'))
                    self.wfile.write(bytes('</ul>', encoding='utf8'))
            else:
                print('ELSE')
        else:
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Generic Website</h1>')
            self.wfile.write(bytes("""<form>
              Query:<br>
              <input type="text" name="q" value=""><br>
              <input type="submit" value="Submit">
            </form>""", encoding='utf8'))


def run(server_class=http.server.HTTPServer, handler_class=http_handler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

run()