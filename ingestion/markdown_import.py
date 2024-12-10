from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os
from general.db import get_or_create_table
import general.models as models
from ingestion.tags import extract_tags_from_filename, extract_tags_from_text
import sys
from general.logger import logger


def import_file(path, root_path, model, content_path=None, modif_time=None):
  doc_table=get_or_create_table(table_name=models.TABLE_DOCUMENTS, schema=models.Document)
  if content_path == None:
    content_path = path
  text = ""
  relpath = os.path.relpath(path, root_path)
  logger.info(f"Ingesting {path}")
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
  logger.info(f" with {nb_chunks} chunks ")
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
    logger.info(f"{relpath}[{index}/{nb_chunks}]")
    logger.debug(f"  text:\n {chunk}")
    embed = ollama.embeddings(model=model, prompt=chunk)['embedding']

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
    logger.debug("---")
    logger.debug("\nDocument text_unit:")
    logger.debug(f"ID: {text_unit.id}")
    logger.debug(f"Text: {text_unit.text[:100]}...")
    logger.debug(f"Vector: {text_unit.text_embedding[:5]}...")
    logger.debug(f"Source Root: {document.root}")
    logger.debug(f"Source Relative Path: {document.relative_path}")
    logger.debug(f"Source Full Path: {document.fullpath}")
    logger.debug(f"Import Time: {document.import_time}")
    logger.debug(f"Chunk Index: {text_unit.chunk_index}")
    logger.debug(f"Number of Chunks: {len(document.text_unit_ids)}")

  # timing log
  import_time=(time.time() - starttime)
  logger.info((f" done in: {import_time} seconds"))

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
      logger.info("no change, skipping")
      return {
        "message": "no change, skipping",
        "file": relpath,
      }
    else:
      logger.info(f"File has changed, deleting existing DB entries for: {relpath}")
      table.delete(f"relative_path = '{relpath}'")
