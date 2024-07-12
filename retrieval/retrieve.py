from utilities import getconfig
from retrieval.search_db import search_db
from retrieval.improve_results import improve_results

def retrieve(query, embedmodel, table):
  results = search_db(query=query, embedmodel=embedmodel, table=table)
  print(f"notes returned:")
  for entry in results:
    print(f"- {entry['id']}")
  return build_context(db_results=results, query=query, embedmodel=embedmodel, table=table)

def build_context(db_results, query, embedmodel, table):
  context = ""
  db_results = improve_results(db_results=db_results, query=query, embedmodel=embedmodel, table=table)
  for entry in db_results:
    context += f"{entry['document']} "
  return context