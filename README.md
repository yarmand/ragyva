# ragyva
my personal take on RAG to manage my personal notes

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
Make sure you have the models listed in config.ini. so for nomic-embed-text, run `ollama pull nomic-embed-text`. Update the config to show whatever models you want to use.

### chromaDB
```
docker compose up -d chromadb
```
## import notes
- put some md files in the `docs` folder
- generate `sourcedocs.txt`
    `find ./docs -t f -name '*.md'`
- Import the docs: 
    `python3 import.py`

**TODO:** (not great as it requires python language tool, lets switch to a typescript import)

## use notes
- Perform a search: 
    `python3 search.py <yoursearch>`
- chat with notes
    `python3 chat.py`

**TODO:** As we move import to typescript, lets do search and chat as well
