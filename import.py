#!/usr/bin/env python3

from config import getconfig
from db_import.markdown_import import import_file
from db_import.doc_model import DocModel
import ollama, time
import lancedb
import sys
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument('--collection-name', default=getconfig("lancedb", "doc_table"), help='Specify the collection name to import to in the vector database.')
parser.add_argument('--delete-collection', action='store_true', help='Delete the collection before importing.')
args = parser.parse_args()
collectionname = args.collection_name
delete_collection = args.delete_collection

# initialize DB table
db = lancedb.connect(getconfig("lancedb","data_file"))
if delete_collection:
  db.drop_table(name=collectionname, ignore_missing=True)
doc_table = False
# find existing table
for t in db.table_names():
  if t == collectionname:
    doc_table = db.open_table(collectionname)
# create table if it doesn't exist
if doc_table == False:
  doc_table = db.create_table(collectionname, schema=DocModel.to_arrow_schema()) 


embedmodel = getconfig("main", "embedmodel")
starttime = time.time()
with sys.stdin as f:
  lines = f.readlines()
  for filename in lines:
    filename = filename.rstrip()
    filename = filename.replace(' \n', '')
    filename = filename.replace('%0A', '')
    # artificial limit to prevent large files from being imported
    import_file(
      path=filename, 
      root_path=getconfig("import", "notes_root_path"), 
      model=embedmodel, 
      table=doc_table
    )
    
print("\n---Total--- %s seconds ---" % (time.time() - starttime))

