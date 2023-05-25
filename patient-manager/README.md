# Development within Patient-Manager

```
virtualenv .env --python=python3.8
. .env/bin/activate
pip install poetry
poetry install
```

Install packages for linting:
```
poetry install --with lint
```
Replace `lint` by `test` if you need to install test dependencies only.

Install packages for linting and testing:
```
poetry install --with lint --with test
```

# Running the server

```
uvicorn scanhub.main:app --reload --port 8000
```


# Database

The postgres database, which is created within the patient-manager, can be reached by the following address.

```
http://localhost:8080
```

Login information for the database: To be updated...

|                       |                                   |
| :---                  |                              ---: |
| Datenbank System      | PostgreSQL                        |
| Server                | postgres                          |
| Benuter               | brainLink                         |
| Passwort              | brainLinkIstCool2022UndLecker     |
| Datenbank             | -                                 |
