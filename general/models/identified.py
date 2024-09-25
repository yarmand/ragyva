from lancedb.pydantic import LanceModel

class Identified(LanceModel):
  """A protocol for an item with an ID."""

  id: str
  """The ID of the item."""

  short_id: str | None
  """Human readable ID used to refer to this object in prompts or texts displayed to users, such as in a report text (optional)."""
