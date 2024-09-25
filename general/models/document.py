from .named import Named
from lancedb.pydantic import Any

TABLE_DOCUMENTS = "documents"

class Document(Named):
  """A protocol for a document in the system."""
  
  fullpath: str | None = None
  """The file of hte document if the document comes from a file"""
  root: str
  """Root path where all the documents are"""
  relative_path: str
  """path to document from root"""
  import_time: float
  """when the document was last processed. USed to avoid re-ingest a document aht didn't change"""

  text_unit_ids: list[str]
  """list of text units in the document."""

  tag_ids: list[str]
  """Tags defined in the document meta-data section, at the top."""

  raw_content: str = ""
  """The raw text content of the document."""

  summary: str | None = None
  """Summary of the document (optional)."""

  summary_embedding: list[float] | None = None
  """The semantic embedding for the document summary (optional)."""

  raw_content_embedding: list[float] | None = None
  """The semantic embedding for the document raw content (optional)."""

  attributes: dict[str, Any] | None = None
  """A dictionary of structured attributes such as author, etc (optional)."""
