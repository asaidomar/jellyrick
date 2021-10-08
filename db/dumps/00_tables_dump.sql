-- ****************** JellyRick: MySQL ******************;
-- ***************************************************;


-- ************************************** `comment`

CREATE TABLE IF NOT EXISTS `comment`
(
    `comment_id`   int unsigned NOT NULL AUTO_INCREMENT,
    `comment_text` varchar(200) NOT NULL,

    PRIMARY KEY (`comment_id`),
    UNIQUE KEY `name` (`comment_text`)
);


-- ************************************** `episode`

CREATE TABLE IF NOT EXISTS `episode`
(
    `episode_id`   int unsigned NOT NULL AUTO_INCREMENT,
    `episode_name` varchar(50)  NOT NULL,
    `comment_id`   int unsigned NULL,

    PRIMARY KEY (`episode_id`),
    UNIQUE KEY `name` (`episode_name`),
    KEY `FK_episode_comment_id` (`comment_id`),
    CONSTRAINT `FK_constr_episode_comment` FOREIGN KEY `FK_episode_comment_id` (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ************************************** `character`

CREATE TABLE IF NOT EXISTS `character`
(
    `character_id`   int unsigned NOT NULL AUTO_INCREMENT,
    `character_name` varchar(50)  NOT NULL,
    `comment_id`     int unsigned NULL,

    PRIMARY KEY (`character_id`),
    UNIQUE KEY `name` (`character_name`),
    KEY `FK_character_comment_id` (`comment_id`),
    CONSTRAINT `FK_character_comment` FOREIGN KEY `FK_character_comment_id` (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ************************************** `episode_character_appearance`

CREATE TABLE IF NOT EXISTS `episode_character_appearance`
(
    `comment_id` int unsigned NULL,
    `character`  int unsigned NOT NULL,
    `episode`    int unsigned NOT NULL,

    PRIMARY KEY (`character`, `episode`),
    KEY `FK_constr_ep_ap_char` (`character`),
    CONSTRAINT `FK_constr_episode_appearance_character` FOREIGN KEY `FK_constr_ep_ap_char` (`character`) REFERENCES `character` (`character_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    KEY `FK_constr_ep_ap_com` (`comment_id`),
    CONSTRAINT `FK_constr_episode_character_appearance_comment` FOREIGN KEY `FK_constr_ep_ap_com` (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    KEY `FK_constr_ep_ap_ep_fk` (`episode`),
    CONSTRAINT `FK_constr_episode_appearance_episode` FOREIGN KEY `FK_constr_ep_ap_ep_fk` (`episode`) REFERENCES `episode` (`episode_id`) ON DELETE CASCADE ON UPDATE CASCADE
);
