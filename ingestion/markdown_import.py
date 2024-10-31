from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os
from general.models import DocModel
from ingestion.tags import extract_tags_from_filename, extract_tags_from_text
import sys


def import_file(path, root_path, model, table, content_path=None, modif_time=None):
  if content_path == None:
    content_path = path
  text = ""
  relpath = os.path.relpath(path, root_path)

  if skip_this_file(path=path, relpath=relpath, modif_time=modif_time, table=table):
    return

  ###
  # ingest file
  ###
  starttime = time.time()
  with open(content_path, 'rb') as f:
    text = f.read().decode('utf-8')
  splitter = MarkdownTextSplitter(chunk_size = 500, chunk_overlap=0)
  documents = splitter.create_documents([text])
  nb_chunks = len(documents)
  print(f"with {nb_chunks} chunks ", file=sys.stderr)
  doc_tags_names = []
  doc_tags_names += extract_tags_from_filename(path)
  #doc_tags_names += extract_tags_from_header(path)

  for index, document in enumerate(documents):
    chunk = document.page_content
    chunk_tags_names = extract_tags_from_text(chunk)
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
      doc_tags=doc_tags_names,
      chunk_tags=chunk_tags_names,
    )
    table.add([data])

  # Print data nicely to stderr
  print("\nDocument Data:", file=sys.stderr)
  print(f"ID: {data.id}", file=sys.stderr)
  print(f"Text: {data.text[:100]}...", file=sys.stderr)  # Print first 100 characters of the text
  print(f"Vector: {data.vector[:5]}...", file=sys.stderr)  # Print first 5 elements of the vector
  print(f"Source Root: {data.source_root}", file=sys.stderr)
  print(f"Source Relative Path: {data.source_relative_path}", file=sys.stderr)
  print(f"Source Full Path: {data.source_fullpath}", file=sys.stderr)
  print(f"Import Time: {data.import_time}", file=sys.stderr)
  print(f"Chunk Index: {data.chunk_index}", file=sys.stderr)
  print(f"Number of Chunks: {data.nb_chunks}", file=sys.stderr)
  print(f"Links: {data.links}", file=sys.stderr)
  #print(f"Document Tags: {data.doc_tags_names}", file=sys.stderr)
  #print(f"Chunk Tags: {data.chunk_tags_names}", file=sys.stderr)

  # timing log
  import_time=(time.time() - starttime)
  print((" < %s seconds >" % import_time), file=sys.stderr)

  return {
    "message": "import OK",
    "file": relpath,
    "import_time": import_time,
  }

def skip_this_file(path, relpath, table, modif_time=None):
  # # retreive existing document
  existing_doc = False
  docs = table.search().where(f"source_relative_path =  '{relpath}'", prefilter=True).to_pandas()
  if len(docs['id']) > 0:
    existing_doc = docs["id"][0]
  # skip if document did not change
  if existing_doc:
    last_change = modif_time
    if modif_time == None:
      last_change = os.path.getmtime(path)
    if last_change < docs["import_time"][0]:
      print("no change, skipping", file=sys.stderr)
      return {
        "message": "no change, skipping",
        "file": relpath,
      }
    else:
      print((f"File has changed, deleting existing DB entries for: {relpath}"), file=sys.stderr)
      table.delete(f"source_relative_path = '{relpath}'")
