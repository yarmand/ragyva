#!/usr/bin/env python3

from utilities import getconfig
from db_import.file_import import import_file
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
    import_file(filename, embedmodel, collection)
    
print("--- %s seconds ---" % (time.time() - starttime))

