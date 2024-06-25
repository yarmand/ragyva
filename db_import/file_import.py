from .readtext import readtext
from mattsollamatools import chunker, chunk_text_by_sentences
import ollama

def import_file(filename, embedmodel, collection):
  text = readtext(filename)
  chunks = chunk_text_by_sentences(source_text=text, sentences_per_chunk=7, overlap=0 )
  print(f"with {len(chunks)} chunks")
  for index, chunk in enumerate(chunks):
    embed = ollama.embeddings(model=embedmodel, prompt=chunk)['embedding']
    print(".", end="", flush=True)
    collection.add([filename+str(index)], [embed], documents=[chunk], metadatas={"source": filename})
