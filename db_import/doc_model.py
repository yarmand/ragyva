from lancedb.pydantic import LanceModel, Vector

class DocModel(LanceModel):
  vector: Vector(768)
  text: str
  id: str
  source: str
  import_time: float
  chunk_index: int
  nb_chunks: int