from lancedb.pydantic import LanceModel, Vector
from enum import Enum

class TableNames:
  DOC_MODEL = "doc_model"
  TAG_MODEL = "tag_model"
  PERSON_MODEL = "person_model"
  COMMUNITY_MODEL = "community_model"
  CHAT_MODEL = "chat"


class DocModel(LanceModel):
  vector: Vector(768)
  id: str
  text: str
  source_fullpath: str
  source_root: str
  source_relative_path: str
  import_time: float
  chunk_index: int
  nb_chunks: int
  links: list[str]
  doc_tags: list[str]
  chunk_tags: list[str]

class TagModel(LanceModel):
  vector: Vector(768)
  id: str
  text: str

class PersonModel(LanceModel):
  id: str
  name: str
  aliases: list

class CommunityModel(LanceModel):
  vector: Vector(768)
  id: str
  text: str

class Chat(LanceModel):
  id: str
  messages: str
