from utilities import getconfig
from retrieval.search_db import search_db
from retrieval.improve_results import improve_results

def retrieve(query, embedmodel, collection):
  results = search_db(query=query, embedmodel=embedmodel, collection=collection)
  print(f"notes returned:")
  for entry in results:
    print(f"- {entry['id']}")
  return build_context(db_results=results, query=query, embedmodel=embedmodel, collection=collection)

def build_context(db_results, query, embedmodel, collection):
  context = ""
  db_results = improve_results(db_results=db_results, query=query, embedmodel=embedmodel, collection=collection)
  for entry in db_results:
    context += f"{entry['document']} "
  return context