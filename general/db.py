import lancedb
import os
from general.models import DocModel, TableNames
from general.config import getconfig
import sys

def get_db():
  return lancedb.connect(getconfig("lancedb","data_dir"))

def get_table(db=get_db(), tablename=TableNames.DOC_MODEL):
  return db.open_table(tablename)

def get_or_create_table(table_name, delete_table=False, db=get_db(), schema=DocModel.to_arrow_schema()):
  # initialize DB table
  if delete_table:
    db.drop_table(name=table_name, ignore_missing=True)
  doc_table = False
  try:
    doc_table = get_table(db=db, tablename=table_name)
  except Exception as e:
    print(f"Error occurred: {e}. Creating table {table_name}.", file=sys.stderr)
    doc_table = db.create_table(table_name, schema=schema)
  return doc_table
