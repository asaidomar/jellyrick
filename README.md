# Jellyrick

API to post comments about Rick & Morty universe

## Dev quick start 🚀

Prerequisites:

- git installed
- Linux, Mac or WSL environment
- docker and docker-compose installed : https://docs.docker.com/compose/install/
- python3, python3-pip installed

```bash
git clone git@github.com:benjmathias/jellyrick.git
cd jellyrick
docker-compose -f dev.docker-compose.yml up
```

## Database usage 📙

Follow the "dev quick start" step above first !

- Get data from api with a python script ([script](./db/script/write_from_web_to_json.py)) :

```bash
cd db/script
chmod +x write_from_web_to_json.py
./write_from_web_to_json.py "../data_source"
```

- Script usage to insert data from json file to DB ([script](./db/script/insert_from_json_to_db.py)) :

```bash
pip3 install mysql-connector-python
cd db/script
chmod +x insert_from_json_to_db.py
./insert_from_json_to_db.py "universe" "root" "root" "../data_source"
```

You can check with adminer front that the data has been inserted, connect with "universe" database and "root" "root"
credentials :

- http://localhost/?server=db&username=root&db=universe&select=character

To connect with mysql-client cli to DB from host :

```bash
mysql -u root -p'root' -h 127.0.0.1 -D universe
```

To connect with mysql-client cli to DB from inside the API container :

```bash
mysql -u rick -p'morty' -h db -D universe
```

## Tasks

- [x]  Init base files (15 minutes)
    - [x]  Create project on github
    - [x]  Add readme
    - [x]  Add .gitignore
    - [x]  Add CHANGELOG
- [ ]  Feature 1
    - [x]  DB dev environment
        - [x]  Dockerfile
        - [x]  docker-compose
    - [x]  Init the db structure, dump it, put the dump in db container entrypoint
    - [x]  Retrieve characters and episodes data from the web (rickandmortyapi.com) and write it to
      JSON : ([script](./db/script/write_from_web_to_json.py), [data](./db/rick_data.json))
    - [x]  Python import script ([script](./db/script/insert_from_json_to_db.py))
    - [ ]  Fastapi base structure
    - [ ]  api dev environment
        - [ ]  Dockerfile
        - [ ]  docker-compose
    - [ ]  Add db insertion script at the beginning of the dev entrypoint of the API
    - [ ]  Write test for the two routes (retrieve data from mysql)
    - [ ]  Write the two routes (retrieve data from mysql)