#!/usr/bin/env python3

from utilities import readtext, getconfig
from mattsollamatools import chunker, chunk_text_by_sentences
import ollama, chromadb, time
import sys
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--collection-name', default=getconfig("main", "chroma_collection"), help='Specify the collection name to import to in the vector database.')
args = parser.parse_args()

collectionname = args.collection_name

chroma = chromadb.HttpClient(host=getconfig("main", "chroma_host"), port=getconfig("main","chroma_port"))
print(chroma.list_collections())
if any(collection.name == collectionname for collection in chroma.list_collections()):
  print('deleting collection')
  chroma.delete_collection(collectionname)
collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})
embedmodel = getconfig("main", "embedmodel")
starttime = time.time()
with sys.stdin as f:
  lines = f.readlines()
  for filename in lines:
    text = readtext(filename)
    chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
    print(f"with {len(chunks)} chunks")
    for index, chunk in enumerate(chunks):
      embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
      print(".", end="", flush=True)
      collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
    
print("--- %s seconds ---" % (time.time() - starttime))

