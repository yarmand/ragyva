from config import getconfig
from retrieval.search_db import search_db
from retrieval.improve_results import improve_results
import sys
import json

def retrieve(query, embedmodel, table):
  results = search_db(query=query, embedmodel=embedmodel, table=table)
  print(f"notes returned:", file=sys.stderr)
  for entry in results:
    print(f"- {entry['id']}", file=sys.stderr)
  return improve_results(db_results=results, query=query, embedmodel=embedmodel, table=table)