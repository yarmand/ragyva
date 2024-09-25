from .named import Named
from lancedb.pydantic import Any

TABLE_COMMUNITIES = "communities"

class Community(Named):
  """A protocol for a community in the system."""

  level: str = ""
  """Community level."""

  entity_ids: list[str] | None = None
  """List of entity IDs related to the community (optional)."""

  relationship_ids: list[str] | None = None
  """List of relationship IDs related to the community (optional)."""

  covariate_ids: dict[str, list[str]] | None = None
  """Dictionary of different types of covariates related to the community (optional), e.g. claims"""

  attributes: dict[str, Any] | None = None
  """A dictionary of additional attributes associated with the community (optional). To be included in the search prompt."""
