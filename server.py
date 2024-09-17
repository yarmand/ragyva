#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import subprocess
import sys

class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if self.path == '/import':
      self.handle_import()
    elif self.path == '/retrieve':
      self.handle_retrieve()
    else:
      self.send_response(404)
      self.end_headers()

  def handle_import(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    params = json.loads(post_data)
    path = params.get('path')

    if not path:
      self.send_response(400)
      self.end_headers()
      self.wfile.write(b'{"error": "Path parameter is missing"}')
      return

    print("YOOOOOO")

    with subprocess.Popen(['python3', 'import.py', '--path', path], stderr=subprocess.PIPE, text=True) as proc:
      for line in proc.stderr:
        print(line, file=sys.stderr)
    # tags = result.stdout.strip()

    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    response = {'import': 'ok'}
    # response = {'tags': tags}
    self.wfile.write(json.dumps(response).encode('utf-8'))

  def handle_retrieve(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    params = json.loads(post_data)
    query = params.get('query')
    tags = params.get('tags')

    if not query or not tags:
      self.send_response(400)
      self.end_headers()
      self.wfile.write(b'{"error": "Query or tags parameter is missing"}')
      return

    # Dummy response for demonstration purposes
    response = {
      'collection': [
        {'text': 'Example text 1', 'links': ['http://example.com/1']},
        {'text': 'Example text 2', 'links': ['http://example.com/2']}
      ]
    }

    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8824):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print(f'Starting httpd server on port {port}')
  httpd.serve_forever()

if __name__ == '__main__':
  run()