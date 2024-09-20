import lancedb
import os
from models import DocModel
from config import getconfig

def get_db():
  return lancedb.connect(getconfig("lancedb","data_file"))

def get_table(db=get_db(), tablename=getconfig("lancedb", "doc_table")):
  return db.open_table(tablename)

def get_or_create_table(table_name, delete_table=False, db=get_db(), schema=DocModel.to_arrow_schema()):
  # initialize DB table
  if delete_table:
    db.drop_table(name=table_name, ignore_missing=True)
  doc_table = False
  try:
    doc_table = get_table(db=db, tablename=table_name)
  except Exception as e:
    print(f"Error occurred: {e}. Creating table {table_name}.")
    doc_table = db.create_table(table_name, schema=schema)
  return doc_table
  # # find existing table
  # for t in db.table_names():
  #   if t == table_name:
  #     doc_table = db.open_table(table_name)
  # # create table if it doesn't exist
  # if doc_table == False:
  #   doc_table = db.create_table(table_name, schema=schema) 
  # return doc_table
