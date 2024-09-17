from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os
from db_import.doc_model import DocModel
import sys


def import_file(path, root_path, model, table):
  text = ""
  relpath = os.path.relpath(path, root_path)
  print(f"-- {relpath} --", file=sys.stderr)

  # # retreive existing document
  existing_doc = False
  docs = table.search().where(f"source =  '{path}'", prefilter=True).to_pandas()
  if len(docs['id']) > 0:
    existing_doc = docs["id"][0]
  # skip if document did not change
  if existing_doc:
    last_change = os.path.getmtime(path)
    if last_change < docs["import_time"][0]:
      print("no change, skipping", file=sys.stderr)
      return

  starttime = time.time()
  with open(path, 'rb') as f:
    text = f.read().decode('utf-8')
  splitter = MarkdownTextSplitter(chunk_size = 40, chunk_overlap=0)
  documents = splitter.create_documents([text])
  nb_chunks = len(documents)
  print(f"with {nb_chunks} chunks ", file=sys.stderr)
  for index, document in enumerate(documents):
    chunk = document.page_content
    # print(f"{relpath}[{index}]: {chunk}", file=sys.stderr)
    embed = ollama.embeddings(model=model, prompt=chunk)['embedding']
    print(".", end="", flush=True, file=sys.stderr)

    data = DocModel(
      vector= embed,
      text=chunk,
      id=f"{relpath}_{index}",
      source=relpath,
      import_time=starttime,
      chunk_index=index,
      nb_chunks=nb_chunks,
      links=[]
    )
    if existing_doc:
      table.update(where=f"id = {data.id}", values=data)
    else:
      table.add([data])
  print(" < %s seconds >" % (time.time() - starttime), file=sys.stderr)
