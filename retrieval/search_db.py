import ollama
from general.config import getconfig
import sys

def search_db(query, embedmodel, table):
  queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
  db_results = table.search(queryembed).limit(int(getconfig("retrieval", "nb_db_results"))).to_pandas()
  results = []
  for i in range(len(db_results["id"])):
    entry = {
      "id": db_results["id"][i],
      "document": db_results["text"][i],
    }
    results.append(entry)
  print(f"results: {results}", file=sys.stderr)
  return results