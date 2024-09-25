from .named import Named
from lancedb.pydantic import Any

TABLE_COMMUNITIES = "communities"

class Community(Named):
  """A protocol for a community in the system."""

  level: str = ""
  """Community level."""

  entity_ids: list[str] = []
  """List of entity IDs related to the community (optional)."""

  relationship_ids: list[str] = []
  """List of relationship IDs related to the community (optional)."""

  attributes_keys: list[str] = []
  attributes_values: list[str] = []
  """A dictionary of additional attributes associated with the community (optional). To be included in the search prompt."""
