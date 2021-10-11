LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user`
    DISABLE KEYS */;
INSERT INTO `user`
VALUES ('administrator', 'root', 'root@example.com',
        '$2b$12$aCTNUC0Cn.nCgJLb.aV2BOdf741P6YfLQGwNeCrfbd8JT.pD0Gx72', 0, 1, 0, 0),
       ('johndoe', 'John Doe', 'johndoe@example.com',
        '$2b$12$p/jVI4OUMvvQjXrQsnFXj.Qh0C6aWrmACwCTeQXEOh8nN8SX59R5e', 0, 0, 0, 0),
       ('moderator', 'modo', 'modo@example.com',
        '$2b$12$9yiWGx1WME6kuigUp3Q6vuEg3DfKpGVmrHGobpgRN518Nt9tVl.Sa', 0, 0, 0, 1),
       ('ben', 'benjamin mathias', 'benjamin.mathias@dataperl.com',
        '$2b$12$p/jVI4OUMvvQjXrQsnFXj.Qh0C6aWrmACwCTeQXEOh8nN8SX59R5e', 0, 1, 0, 0);
/*!40000 ALTER TABLE `user`
    ENABLE KEYS */;
UNLOCK TABLES;
