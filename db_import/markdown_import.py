from langchain.text_splitter import MarkdownTextSplitter
import ollama, time, os

def import_file(filename, embedmodel, collection):
  text = ""
  print(f"-- {filename} --")

  # # retreive existing document
  existing_doc = False
  docs = collection.get(include=["metadatas"], where={ "source": filename })
  if len(docs['ids']) > 0:
    existing_doc = docs["ids"][0]
  # skip if document did not change
  if existing_doc:
    last_change = os.path.getmtime(filename)
    if last_change < docs["metadatas"][0]["import_time"]:
      print("no change, skipping")
      return

  starttime = time.time()
  with open(filename, 'rb') as f:
    text = f.read().decode('utf-8')
  splitter = MarkdownTextSplitter(chunk_size = 40, chunk_overlap=0)
  documents = splitter.create_documents([text])
  print(f"with {len(documents)} chunks ", end="", flush=True)
  for index, document in enumerate(documents):
    chunk = document.page_content
    # print(f"{filename}[{index}]: {chunk}")
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
    print(".", end="", flush=True)
    metadatas = {"source": filename, "import_time": starttime}
    if existing_doc:
      collection.update(ids=[existing_doc], 
                        embeddings=[embed], 
                        documents=[chunk], 
                        metadatas=[metadatas])
    else:
      collection.add(ids=[filename+str(index)], 
                    embeddings=[embed], 
                    documents=[chunk], 
                    metadatas=[metadatas]
                    )
  print(" < %s seconds >" % (time.time() - starttime))
  