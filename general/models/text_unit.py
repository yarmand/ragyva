from .identified import Identified
from lancedb.pydantic import Any

TABLE_TEXT_UNITS = "text_units"

class TextUnit(Identified):
  """A protocol for a TextUnit item in a Document database."""

  text: str
  """The text of the unit."""

  text_embedding: list[float] | None = None
  """The text embedding for the text unit (optional)."""

  link_ids: list[str]
  """Wiki type links extracted from this chunk."""
  tag_ids: list[str]
  """Tgs extracted from this chunk"""

  entity_ids: list[str] | None = None
  """List of entity IDs related to the text unit (optional)."""

  relationship_ids: list[str] | None = None
  """List of relationship IDs related to the text unit (optional)."""

  n_tokens: int | None = None
  """The number of tokens in the text (optional)."""

  document_ids: list[str] | None = None
  """List of document IDs in which the text unit appears (optional)."""

  attributes_keys: list[str] | None = None
  attributes_values: list[str] | None = None
  """A dictionary of additional attributes associated with the text unit (optional)."""
