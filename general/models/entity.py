from .named import Named
from lancedb.pydantic import Any

TABLE_ENTITIES = "entities"

class Entity(Named):
  """A protocol for an entity in the system."""

  type: str
  """Type of the entity (can be any string, optional)."""

  description: str = ""
  """Description of the entity (optional)."""

  description_embedding: list[float] = []
  """The semantic (i.e. text) embedding of the entity (optional)."""

  name_embedding: list[float] = []
  """The semantic (i.e. text) embedding of the entity (optional)."""

  graph_embedding: list[float] = []
  """The graph embedding of the entity, likely from node2vec (optional)."""

  community_ids: list[str] = []
  """The community IDs of the entity (optional)."""

  text_unit_ids: list[str] = []
  """List of text unit IDs in which the entity appears (optional)."""

  document_ids: list[str] = []
  """List of document IDs in which the entity appears (optional)."""

  rank: int | None = 1
  """Rank of the entity, used for sorting (optional). Higher rank indicates more important entity. This can be based on centrality or other metrics."""

  attributes_keys: list[str] = []
  attributes_values: list[str] = []
  """Additional attributes associated with the entity (optional), e.g. start time, end time, etc. To be included in the search prompt."""
