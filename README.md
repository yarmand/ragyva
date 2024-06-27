# ragyva

my personal take on RAG to manage my personal notes

__disclaimer__: Kudos to @technovangelist for [their rag tutorial](https://github.com/technovangelist/videoprojects/tree/main/2024-04-04-build-rag-with-python) that I used to bootsrtap this repo.

## install and requirements

### devcontainer

lets use the devcontainer, it will install everything and will serve as base for final distribution.

start it with VSCode or run

```
devcontainer up --workspace-folder $(pwd)
```

### ollama

run [ollama](https://ollama.com/) on your machine.

### models

Make sure you have the models listed in config.ini. so for `nomic-embed-text`

```
ollama pull nomic-embed-text
```

Update the config to show whatever models you want to use.
A good small model for chat is `phi3:instruct`

```
ollama pull phi3:instruct
```

### chromaDB

```
docker compose up -d chromadb
```

choma DB will run on <http://localhost:8000>

## import notes

```
find ./docs -name '*.md' | import.py
```

You can specify the collection name with `--collection-name`
(see details with `import.py -h`)

## chat with notes

```
chat.py
```

# TODO

## improve import

- find the right balance of chunk size
- add significant meta-data
  - note / file the chunk is coming from
  - current title
  - significant objects founf in the chunk
    - dates
    - people
    - tags
- split using titles
- Embed Images
  - describe images
  - extract keywords from diagram
- graphDB associated with notes
  - significant meta-data
  - references from note to notes

## improve retrieval

- return full note instead of chuncks as an option
- reuturn full paragragh instead of chunk
- add layer to filter returned data and eliminate not relevant
- iptimize model temperature on retreival filter
- Analyse prompt to distinguish content questions from dataset question (ex: how many documents with ...)

## improve generation

- prompt engineering on template.
  - where to put hte retreived data
  - where to insert the user query
- optimize model temperature on response generation

## Notes Agents

- Allow to perform actions on notes
- Input then organize
  - user to free input of note
  - on save, analyse and propose to organise note following PARA ( Projects, Areas, Resources, Archives)
