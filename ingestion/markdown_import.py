from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os
from models import DocModel
import sys


def import_file(path, root_path, model, table):
  text = ""
  relpath = os.path.relpath(path, root_path)

  if skip_this_file(path=path, relpath=relpath, table=table):
    return

  ###
  # ingest file
  ###
  starttime = time.time()
  with open(path, 'rb') as f:
    text = f.read().decode('utf-8')
  splitter = MarkdownTextSplitter(chunk_size = 500, chunk_overlap=0)
  documents = splitter.create_documents([text])
  nb_chunks = len(documents)
  print(f"with {nb_chunks} chunks ", file=sys.stderr)
  doc_tags = []
  doc_tags += extract_tags_from_filename(path)
  for index, document in enumerate(documents):
    chunk = document.page_content
    # print(f"{relpath}[{index}]: {chunk}", file=sys.stderr)
    embed = ollama.embeddings(model=model, prompt=chunk)['embedding']
    print(".", end="", flush=True, file=sys.stderr)

    data = DocModel(
      vector= embed,
      text=chunk,
      id=f"{relpath}_{index}",
      source_root=root_path,
      source_relative_path=relpath,
      source_fullpath=path,
      import_time=starttime,
      chunk_index=index,
      nb_chunks=nb_chunks,
      links=[],
      doc_tags=doc_tags,
      chunk_tags=[],
    )
    table.add([data])

  # timing log
  import_time=(time.time() - starttime)
  print(" < %s seconds >" % import_time)

  return {
    "message": "import OK",
    "file": relpath,
    "import_time": import_time,
  }

def skip_this_file(path, relpath, table)
  # # retreive existing document
  existing_doc = False
  docs = table.search().where(f"source_relative_path =  '{relpath}'", prefilter=True).to_pandas()
  if len(docs['id']) > 0:
    existing_doc = docs["id"][0]
  # skip if document did not change
  if existing_doc:
    last_change = os.path.getmtime(path)
    if last_change < docs["import_time"][0]:
      print("no change, skipping", file=sys.stderr)
      return {
        "message": "no change, skipping",
        "file": relpath,
      }
    else:
      print(f"File has changed, deleting existing DB entries for: {relpath}")
      table.delete(f"source_relative_path = '{relpath}'")
