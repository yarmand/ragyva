#!/usr/bin/env python3

from config import getconfig
from db_import.markdown_import import import_file
import time
import sys
import argparse
from db import get_or_create_table

def import_from_stdin(collectionname, delete_collection):
  embedmodel = getconfig("main", "embedmodel")
  starttime = time.time()
  with sys.stdin as f:
    lines = f.readlines()
    for filename in lines:
      filename = filename.rstrip()
      filename = filename.replace(' \n', '')
      filename = filename.replace('%0A', '')
      import_file(
        path=filename, 
        root_path=getconfig("import", "notes_root_path"), 
        model=embedmodel, 
        table=get_or_create_table(table_name=collectionname, delete_table=delete_collection)
      )
  print("\n---Total--- %s seconds ---" % (time.time() - starttime))

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--collection-name', default=getconfig("lancedb", "doc_table"), help='Specify the collection name to import to in the vector database.')
  parser.add_argument('--delete-collection', action='store_true', help='Delete the collection before importing.')
  args = parser.parse_args()
  collectionname = args.collection_name
  delete_collection = args.delete_collection
  import_from_stdin(collectionname, delete_collection)
