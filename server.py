#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from retrieval.retrieve import retrieve
from db import get_table, get_or_create_table
from models import Chat, TableNames
from ingestion.markdown_import import import_file
from config import getconfig, set_config_file, DEFAULT_CONFIG_FILE
import ollama
import argparse


# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'


class RequestHandler(BaseHTTPRequestHandler):
  def do_POST(self):
    if self.path == '/import':
      self.handle_import()
    elif self.path == '/retrieve':
      self.handle_retrieve()
    else:
      self.send_response(404)
      self.end_headers()

  ###########
  # import
  ###########
  def handle_import(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    params = json.loads(post_data)
    path = params.get('path')
    doc_root = params.get('doc_root')

    if not path:
      self.send_response(400)
      self.end_headers()
      self.wfile.write(b'{"error": "Path parameter is missing"}')
      return

    # TODO: should be optional payload params
    embedmodel = getconfig("main", "embedmodel")

    print(f"{YELLOW}==IMPORT=={RESET_COLOR}")

    result = import_file(
      path=path, 
      root_path=doc_root, 
      model=embedmodel, 
      table=get_or_create_table(table_name=TableNames.DOC_MODEL, delete_table=False)
    )


    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    response = result
    self.wfile.write(json.dumps(response).encode('utf-8'))

  ###########
  # retrieve
  ###########
  def handle_retrieve(self):
    content_length = int(self.headers['Content-Length'])
    post_data = self.rfile.read(content_length)
    params = json.loads(post_data)
    query = params.get('query')
    embedModel = params.get('embedModel')
    mainModel = params.get('mainModel')
    conversationID = params.get('conversationID')

    if not query or not embedModel or not mainModel or not conversationID:
      self.send_response(400)
      self.end_headers()
      self.wfile.write(b'{"error": "Query or tags parameter is missing"}')
      return

    print(f"{YELLOW}==RETRIEVE=={RESET_COLOR}")
    print(f" query:{query}")
    print(f" embedModel:{embedModel}")
    print(f" mainModel:{mainModel}")

    # retreieve significant docs
    docs = retrieve(query, embedmodel=embedModel, table=get_table(TableNames.DOC_MODEL))
    # get the conversation
    system_message = getconfig("chat", "prompt_system")
    chats_table = get_or_create_table(table_name=TableNames.CHAT_MODEL, schema=Chat.to_arrow_schema())
    chats = chats_table.search().where(f"id = '{conversationID}'", prefilter=True).to_pandas()
    chat_messages = []
    if len(chats['id']) == 0:
      chat_messages.append({ "role":"system", "content": system_message })
      messages = json.dumps(chat_messages)
      chat = Chat(
        messages = messages,
        id = conversationID,
      )
      chats_table.add([chat])
    else:
        chat_messages = json.loads(chats['messages'][0])
    # LLM the query with docs as context
    modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"
    chat_messages.append({ "role": "user", "content": modelquery })
    # get a streamed response
    stream = ollama.chat(model=mainModel, messages=chat_messages, stream=True)
    fullResponse = ""
    for chunk in stream:
      if chunk["message"]:
        print(NEON_GREEN + chunk['message']['content'] + RESET_COLOR, end='', flush=True)
        fullResponse = fullResponse + chunk['message']['content']
    print("\n\n")

    # save the conversation
    chat_messages.append({ "role":"assistant", "content":fullResponse})
    messages = json.dumps(chat_messages)
    chat = Chat(
      messages = messages,
      id = conversationID,
    )
    chats_table.delete(f"id = '{conversationID}'")
    chats_table.add([chat])

    # return the full resposne
    response = {"response": fullResponse}
    self.send_response(200)
    self.send_header('Content-Type', 'application/json')
    self.end_headers()
    self.wfile.write(json.dumps(response).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8824):
  server_address = ('', port)
  httpd = server_class(server_address, handler_class)
  print(f'===Starting httpd server on port {port}===')
  httpd.serve_forever()

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', default=DEFAULT_CONFIG_FILE, help='config file to use')
  args = parser.parse_args()
  config_file = args.config
  set_config_file(config_file)
  run()