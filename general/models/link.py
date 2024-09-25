from .identified import Identified

TABLE_LINKS = "links"

class Link(Identified):
  text: str
  """text of the link"""
  source_id: str
  """The chunk where the link belongs"""
  source_doc_id: str
  """The document where the chunk comes from"""
  target_id: str
  """The targeted document"""
