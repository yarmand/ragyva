from .identified import Identified

###
# Named
###
class Named(Identified):
  """A protocol for an item with a name/title."""

  name: str = ""
  """The name/title of the item."""
