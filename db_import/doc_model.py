from lancedb.pydantic import LanceModel, Vector

ModelTypes = {
  "Co": 0,
  "C1": 1,
  "C2": 2,
  "document": 3,
  "document_chunk": 4,
  "person": 5,
  "tag": 6,
}

class DocModel(LanceModel):
  vector: Vector(768)
  text: str
  id: str
  source: str
  import_time: float
  chunk_index: int
  nb_chunks: int
  links: list
