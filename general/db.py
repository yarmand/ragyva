import lancedb
import os
from general.models import DocModel, TableNames
from general.config import getconfig
import sys

def get_db():
  return lancedb.connect(getconfig("lancedb","data_dir"))

def get_table(db=get_db(), tablename=models.TABLE_TEXT_UNITS):
  return db.open_table(tablename)

def get_or_create_table(table_name, delete_table=False, db=get_db(), schema=models.TextUnit.to_arrow_schema()):
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

def find_or_create(table,where, entry):
  """
  Finds an existing record in the specified table that matches the given criteria,
  or creates a new record if none is found.
  Args:
    table (Table): The table object to search within.
    where (str): The lanceDB where condition to match existing records.
    entry (dict): The data to use for creating a new record if no match is found.
  Returns:
    pandas.Series: The first matching record as a pandas Series, or the newly created record.
  """

  l = table.search().where(where).to_list()
  if len(l) == 0:
    print(f"create {table.name} entry: {entry}", file=sys.stderr)
    table.add([entry])
    l = table.search().where(where).to_list()
  if len(l) > 0: 
    return l[0] 
  else: 
    raise ValueError(f"cannot retrieve entry {entry} in table {table.name} after its creation")

