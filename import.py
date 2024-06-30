#!/usr/bin/env python3

from utilities import getconfig
from db_import.markdown_import import import_file
import ollama, chromadb, time
import sys
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--collection-name', default=getconfig("main", "chroma_collection"), help='Specify the collection name to import to in the vector database.')
args = parser.parse_args()

collectionname = args.collection_name

chroma = chromadb.HttpClient(host=getconfig("main", "chroma_host"), port=getconfig("main","chroma_port"))
print(f"find collections: {chroma.list_collections()}")
# if any(collection.name == collectionname for collection in chroma.list_collections()):
#   print(f"deleting collection {collectionname}")
#   chroma.delete_collection(collectionname)
collection = chroma.get_or_create_collection(name=collectionname, metadata={"hnsw:space": "cosine"})
embedmodel = getconfig("main", "embedmodel")
starttime = time.time()
with sys.stdin as f:
  lines = f.readlines()
  for filename in lines:
    filename = filename.rstrip()
    filename = filename.replace(' \n', '')
    filename = filename.replace('%0A', '')
    # artificial limit to prevent large files from being imported
    if os.path.getsize(filename) > 4096:
      continue
    import_file(filename, embedmodel, collection)
    
print("\n---Total--- %s seconds ---" % (time.time() - starttime))

