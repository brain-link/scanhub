## Developing
```
virtualenv .env --python=python3.8
. .env/bin/activate
pip install poetry
poetry install
```

## Running the server
```
uvicorn scanhub.main:app --reload --port 8000
```