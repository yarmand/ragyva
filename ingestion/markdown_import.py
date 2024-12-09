from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os
from general.db import get_or_create_table
import general.models as models
from ingestion.tags import extract_tags_from_filename, extract_tags_from_text
import sys


def import_file(path, root_path, model, content_path=None, modif_time=None):
  doc_table=get_or_create_table(table_name=models.TABLE_DOCUMENTS, schema=models.Document)
  if content_path == None:
    content_path = path
  text = ""
  relpath = os.path.relpath(path, root_path)

  if skip_this_file(path=path, relpath=relpath, modif_time=modif_time, table=doc_table):
    return

  ###
  # ingest file
  ###
  starttime = time.time()
  with open(content_path, 'rb') as f:
    text = f.read().decode('utf-8')
  splitter = MarkdownTextSplitter(chunk_size = 500, chunk_overlap=0)
  chunks = splitter.create_documents([text])
  nb_chunks = len(chunks)
  print(f"with {nb_chunks} chunks ", file=sys.stderr)
  doc_tags_names = []
  doc_tags_names += extract_tags_from_filename(path)
  #doc_tags_names += extract_tags_from_header(path)

  document = models.Document(
    id=f"{relpath}",
    root=root_path,
    relative_path=relpath,
    fullpath=path,
    import_time=starttime,
    nb_chunks=nb_chunks,
    text_unit_ids=[],
  )
  doc_table.add([document])

  text_units_table=get_or_create_table(table_name=models.TABLE_TEXT_UNITS, schema=models.TextUnit)
  for index, c in enumerate(chunks):
    chunk = c.page_content
    chunk_tags_names = extract_tags_from_text(chunk)
    # print(f"{relpath}[{index}]: {chunk}", file=sys.stderr)
    embed = ollama.embeddings(model=model, prompt=chunk)['embedding']
    print(".", end="", flush=True, file=sys.stderr)

    text_unit = models.TextUnit(
      id=f"{relpath}_{index}",
      document_id=document.id,
      text=chunk,
      embedding=embed,
      chunk_index=index,
      links=[],
      doc_tags=doc_tags_names,
      chunk_tags=chunk_tags_names,
    )
    text_units_table.add([text_unit])

    # Print text_unit nicely to stderr
    print("---", file=sys.stderr)
    print("\nDocument text_unit:", file=sys.stderr)
    print(f"ID: {text_unit.id}", file=sys.stderr)
    print(f"Text: {text_unit.text[:100]}...", file=sys.stderr)  # Print first 100 characters of the text
    print(f"Vector: {text_unit.text_embedding[:5]}...", file=sys.stderr)  # Print first 5 elements of the vector
    print(f"Source Root: {document.root}", file=sys.stderr)
    print(f"Source Relative Path: {document.relative_path}", file=sys.stderr)
    print(f"Source Full Path: {document.fullpath}", file=sys.stderr)
    print(f"Import Time: {document.import_time}", file=sys.stderr)
    print(f"Chunk Index: {text_unit.chunk_index}", file=sys.stderr)
    print(f"Number of Chunks: {len(document.text_unit_ids)}", file=sys.stderr)
    # print(f"Links: {text_unit.links}", file=sys.stderr)
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
  docs = table.search().where(f"relative_path =  '{relpath}'", prefilter=True).to_pandas()
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
      table.delete(f"relative_path = '{relpath}'")
