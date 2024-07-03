#!/usr/bin/env python3

import json
import ollama, sys, chromadb
import os
from datetime import datetime
from utilities import getconfig
from retrieval.search_db import search_db


# ANSI escape codes for colors
PINK = '\033[95m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
NEON_GREEN = '\033[92m'
RESET_COLOR = '\033[0m'

mainmodel = getconfig("main", "mainmodel")
embedmodel = getconfig("main", "embedmodel")

chroma = chromadb.HttpClient(host=getconfig("main", "chroma_host"), port=getconfig("main","chroma_port"))
collection = chroma.get_or_create_collection(getconfig("main", "chroma_collection"))

### create conversation dir
conversationsDir = getconfig("main", "conversations_dir")
# Check if the directory already exists
if not os.path.exists(conversationsDir):
    # If not, create the directory
    os.mkdir(conversationsDir)

def saveConversation(history):
  now = datetime.now()
  filename = conversationsDir + "/" + now.strftime("%Y-%m-%d %H:%M:%S") + ".json"
  with open(filename, 'w') as f:
      # Use json.dump to write the array to the file
      json.dump(history, f)

conversation_history = []
system_message = getconfig("chat", "prompt_system")
while True:
  query = input(YELLOW + "Query about your documents (or type 'quit' to exit)\n>>> " + RESET_COLOR)
  if query.lower() == 'quit':
    saveConversation(conversation_history)
    break
    
  docs = search_db(query=query, embedmodel=embedmodel, collection=collection)
  modelquery = f"{query} - Answer that question using the following text as a resource: {docs}"

  conversation_history.append({"role": "user", "content": modelquery})


  print(NEON_GREEN + "\nResponse:\n" + RESET_COLOR)

  messages = [
    {"role": "system", "content": system_message},
    *conversation_history
  ]
  stream = ollama.chat(model=mainmodel, messages=messages, stream=True)
  # stream = ollama.generate(model=mainmodel, prompt=modelquery, stream=True)

  fullResponse = ""
  for chunk in stream:
    if chunk["message"]:
      print(NEON_GREEN + chunk['message']['content'] + RESET_COLOR, end='', flush=True)
      fullResponse = fullResponse + chunk['message']['content']
  print("\n\n")

  conversation_history.append({"role": "assistant", "content": fullResponse})
