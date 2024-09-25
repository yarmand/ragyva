from .identified import Identified

TABLE_LINKS = "links"

class Link(Identified):
  text: str
  """text of the link"""
  source_text_unit_id: str
  """The chunk where the link belongs"""
  source_document_id: str
  """The document where the chunk comes from"""
  target_document_id: str
  """The targeted document"""
