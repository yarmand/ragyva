#!/usr/bin/env python3

from general.config import getconfig, set_config_file,DEFAULT_CONFIG_FILE
from ingestion.markdown_import import import_file
import time
import sys
import argparse
from general.db import get_or_create_table
from general.models import TableNames

def import_a_file(doc_root, filename, delete_collection):
  embedmodel = getconfig("main", "embedmodel")
  result = import_file(
    path=filename, 
    root_path=doc_root, 
    model=embedmodel, 
    table=get_or_create_table(table_name=TableNames.CHUNK_MODEL, delete_table=delete_collection)
  )
  print(result)

def import_from_stdin(doc_root, delete_collection):
  starttime = time.time()
  with sys.stdin as f:
    lines = f.readlines()
    for filename in lines:
      filename = filename.rstrip()
      filename = filename.replace(' \n', '')
      filename = filename.replace('%0A', '')
      import_a_file(doc_root, filename, delete_collection)
  print("\n---Total--- %s seconds ---" % (time.time() - starttime), file=sys.stderr)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', default=DEFAULT_CONFIG_FILE, help='config file to use')
  parser.add_argument('--delete-collection', help='Delete the collection before importing.')
  parser.add_argument('--path', help='Relative path to doc_root to the file to import. If this parameter is not provided, the script will read a list of files to import from stdin')
  parser.add_argument('--doc-root', default=getconfig("ingestion", "notes_root_path") ,help='Folder path where docs are. If this parameter is not provided, the script will use config.ini/import/notes_root_path')
  args = parser.parse_args()
  config_file = args.config
  set_config_file(config_file)
  delete_collection = args.delete_collection
  filename = args.path
  doc_root = args.doc_root
  if filename:
    print(f"Import a single file: root:{doc_root}, file:{filename}", file=sys.stderr)
    import_a_file(doc_root, filename, delete_collection)
  else:
    print("Import filesnames from stdin stdin", file=sys.stderr)
    import_from_stdin(doc_root, delete_collection)
