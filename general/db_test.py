from general.db import get_or_create_table
from general.config import set_config_file, getconfig

class mockDB:
  created_table="no-table-created"
  opened_table="no-table-opened"
  dropped_table="no-table-created"
  tables = []

  def __init__(self, names):
    self.tables = names

  def open_table(self, name):
    self.opened_table = name

  def drop_table(self, name, ignore_missing):
    self.dropped_table = name
    self.tables = []
  
  def create_table(self, name, schema):
    self.created_table = name

  def table_names(self):
    return self.tables

class Test_get_or_create_table():
  def test_create_the_table(self):
    db = mockDB([])
    get_or_create_table("lapin", False, db)
    assert db.created_table == "lapin"

  def test_get_existing_table(self):
    db = mockDB(['lapin'])
    get_or_create_table("lapin", False, db)
    assert db.created_table == "no-table-created"
    assert db.opened_table == "lapin"

  def test_delete_existing_table(self):
    db = mockDB(['lapin'])
    get_or_create_table(table_name="lapin", delete_table=True, db=db)
    assert db.created_table == "lapin"
    assert db.dropped_table == "lapin"

  def test_delete_missing_table(self):
    db = mockDB([])
    get_or_create_table(table_name="lapin", delete_table=True, db=db)
    assert db.created_table == "lapin"
    assert db.dropped_table == "lapin"
