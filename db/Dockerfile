FROM mysql:8.0.26

ADD dumps/00_tables_dump.sql /docker-entrypoint-initdb.d/00_tables_dump.sql
ADD dumps/01_episode.sql /docker-entrypoint-initdb.d/01_episode.sql
ADD dumps/02_character.sql /docker-entrypoint-initdb.d/02_character.sql
ADD dumps/03_episode_character_appearance.sql /docker-entrypoint-initdb.d/03_episode_character_appearance.sql
ADD dumps/03_episode_character_appearance.sql /docker-entrypoint-initdb.d/03_episode_character_appearance.sql
ADD dumps/04_user.sql /docker-entrypoint-initdb.d/04_user.sql
ADD dumps/05_comment.sql /docker-entrypoint-initdb.d/05_comment.sql
ADD dumps/06_episode_comment.sql /docker-entrypoint-initdb.d/06_episode_comment.sql