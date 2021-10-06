# Jellysmack

API to post comments about Rick & Morty universe

## Dev quick start 🚀

```bash
git clone git@github.com:benjmathias/jellyrick.git
cd jellyrick
docker-compose -f dev.docker-compose.yml up
```

## Database usage 📙

From host :

```bash
mysql -u root -p'root' -h 127.0.0.1 -D universe
```

Inside API container :

```bash
mysql -u rick -p'morty' -h db -D universe
```

## Tasks

- [x]  Init base files
    - [x]  Create project on github
    - [x]  Add readme
    - [x]  Add .gitignore
    - [x]  Add CHANGELOG
- [ ]  Feature 1
    - [ ]  DB dev environment
        - [ ]  Dockerfile
        - [ ]  docker-compose
    - [ ]  Init the db structure, dump it, put the dump in
    - [ ]  Retrieve characters and episodes data from the web and write it to JSON
    - [ ]  Python import script
    - [ ]  Fastapi base structure
    - [ ]  api dev environment
        - [ ]  Dockerfile
        - [ ]  docker-compose
    - [ ]  Add db insertion script at the beginning of the dev entrypoint of the API
    - [ ]  Write test for the two routes (retrieve data from mysql)
    - [ ]  Write the two routes (retrieve data from mysql)