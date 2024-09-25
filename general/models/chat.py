from lancedb.pydantic import LanceModel

TABLE_CHATS = "chats"

class Chat(LanceModel):
  id: str
  messages: str
