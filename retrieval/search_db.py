import ollama, chromadb
from utilities import getconfig

def search_db(query, embedmodel, collection):
  queryembed = ollama.embeddings(model=embedmodel, prompt=query)['embedding']
  results = collection.query(query_embeddings=[queryembed], n_results=5)
  print(f"notes returned:")
  for meta in results["metadatas"][0]:
    print(f"- {meta['source']}")
  relevantdocs = results["documents"][0]
  return "\n\n".join(relevantdocs)
