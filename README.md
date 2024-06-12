# ragyva
my personal take on RAG to manage my personal notes

__disclaimer__: Kudos to @technovangelist for [their rag tutorial](https://github.com/technovangelist/videoprojects/tree/main/2024-04-04-build-rag-with-python) that I used to bootsrtap this repo.


## install and requirements
### devcontainer
lets use the devcontainer, it will install everything and will serve as base for final distribution.

start it with VSCode or run
```
devcontainer --workspace-folder $(pwd)
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
choma DB will run on http://localhost:8000


## import notes
- put some md files in the `docs` folder
- generate `sourcedocs.txt`
    `find ./docs -name '*.md' >sourcedocs.txt`
- Import the docs: 
    `python3 import.py`

## use notes
- Perform a search: 
    `python3 search.py <yoursearch>`
- chat with notes
    `python3 chat.py`

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

## improve retreival
- return full note instead of chuncks as an option
- reuturn full paragragh instead of chunk
- add layer to filter returned data and eliminate not relevant
- iptimize model temperature on retreival filter

## improve generation
- prompt engineering on template.
    - where to put hte retreived data
    - where to insert the user query
- optimize model temperature on response generation
