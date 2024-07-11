import ollama
from utilities import getconfig

def search_db(query, embedmodel, collection):
  queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
  db_results = collection.query(query_embeddings=[queryembed], n_results=int(getconfig("retrieval", "nb_db_results")))
  results = []
  for i in range(len(db_results["ids"][0])):
    entry = {
      "id": db_results["ids"][0][i],
      "document": db_results["documents"][0][i],
      "metadata": db_results["metadatas"][0][i]
    }
    results.append(entry)
  print(f"results: {results}")
  return results