from .identified import Identified

###
# Named
###
class Named(Identified):
  """A protocol for an item with a name/title."""

  title: str
  """The name/title of the item."""
