from .identified import Identified
from lancedb.pydantic import Any

TABLE_TEXT_UNITS = "text_units"

class TextUnit(Identified):
  """A protocol for a TextUnit item in a Document database."""

  text: str
  """The text of the unit."""

  text_embedding: list[float] = []
  """The text embedding for the text unit (optional)."""

  link_ids: list[str] = []
  """Wiki type links extracted from this chunk."""
  tag_ids: list[str] = []
  """Tgs extracted from this chunk"""

  entity_ids: list[str] = []
  """List of entity IDs related to the text unit (optional)."""

  relationship_ids: list[str] = []
  """List of relationship IDs related to the text unit (optional)."""

  n_tokens: int = 0
  """The number of tokens in the text (optional)."""

  document_ids: list[str] = []
  """List of document IDs in which the text unit appears (optional)."""

  attributes_keys: list[str] = []
  attributes_values: list[str] = []
  """A dictionary of additional attributes associated with the text unit (optional)."""
