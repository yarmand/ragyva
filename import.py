#!/usr/bin/env python3

from general.config import getconfig, set_config_file,DEFAULT_CONFIG_FILE
from ingestion.markdown_import import import_file
import time
import sys
import argparse
from general.db import get_or_create_table
import general.models as models

def import_a_file(doc_root, filename):
  embedmodel = getconfig("main", "embedmodel")
  result = import_file(
    path=filename, 
    root_path=doc_root, 
    model=embedmodel, 
  )
  print((result), file=sys.stderr)

def import_from_stdin(doc_root):
  starttime = time.time()
  with sys.stdin as f:
    lines = f.readlines()
    for filename in lines:
      filename = filename.rstrip()
      filename = filename.replace(' \n', '')
      filename = filename.replace('%0A', '')
      import_a_file(doc_root, filename)
  print("\n---Total--- %s seconds ---" % (time.time() - starttime), file=sys.stderr)

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', default=DEFAULT_CONFIG_FILE, help='config file to use')
  parser.add_argument('--file', help='import a single file. This is the relative path to doc_root to the file to import. If this parameter is not provided, the script will read a list of files to import from stdin')
  parser.add_argument('--doc-root', default=getconfig("ingestion", "notes_root_path") ,help='Folder path where docs are.')
  args = parser.parse_args()
  config_file = args.config
  set_config_file(config_file)
  filename = args.file
  doc_root = args.doc_root
  if filename:
    print(f"Import a single file: root:{doc_root}, file:{filename}", file=sys.stderr)
    import_a_file(doc_root, filename)
  else:
    print("Import filenames from stdin stdin", file=sys.stderr)
    import_from_stdin(doc_root)
