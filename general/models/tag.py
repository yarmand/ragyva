from .named import Named

TABLE_TAGS = "tags"

class Tag(Named):
  text_unit_ids: list[str]
  document_ids: list[str]
