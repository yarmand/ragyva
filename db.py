import lancedb
import os
from db_import.doc_model import DocModel
from config import getconfig

def get_db():
  return lancedb.connect(getconfig("lancedb","data_file"))

def get_table(db=get_db()):
  return db.open_table(getconfig("lancedb", "doc_table"))

def get_or_create_table(table_name, delete_table=False, db=get_db()):
  # initialize DB table
  if delete_table:
    db.drop_table(name=table_name, ignore_missing=True)
  doc_table = False
  # find existing table
  for t in db.table_names():
    if t == table_name:
      doc_table = db.open_table(table_name)
  # create table if it doesn't exist
  if doc_table == False:
    doc_table = db.create_table(table_name, schema=DocModel.to_arrow_schema()) 
  return doc_table
