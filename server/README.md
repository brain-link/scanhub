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

---

## Docker

Building the docker images
```
docker-compose up -d --build
```

## Database

Use adminer to add data to the postgres database.
```
http://localhost:8080
```
Login information:

|                       |                                   |
| :---                  |                              ---: |
| Datenbank System      | PostgreSQL                        |
| Server                | postgres                          |
| Benuter               | brainLink                         |
| Passwort              | brainLinkIstCool2022UndLecker     |
| Datenbank             | -                                 |

Once you are logged in, select the scanhub database and click on import on the left side to upload sql files.
SQL files are located in `example_data/`. When uploading the files separately, the import order is important,
since some tables depend on each other.

### Import Order

user, patient, site &#8594; device, procedures &#8594; recordings &#8594; site_user, user_patient, site_patient

<br>

> __Note:__ Database tables are generated according to ```database/models.py```. Modifications of the models require a rebuild of the database containers with docker.

<br>
