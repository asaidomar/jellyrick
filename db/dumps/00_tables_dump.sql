-- ****************** JellyRick: MySQL ******************;
-- ***************************************************;


-- ************************************** `episode`

CREATE TABLE IF NOT EXISTS `episode`
(
    `episode_id`   int unsigned NOT NULL AUTO_INCREMENT,
    `episode_name` varchar(50)  NOT NULL,

    PRIMARY KEY (`episode_id`),
    UNIQUE KEY `name` (`episode_name`)
);


-- ************************************** `comment`

CREATE TABLE IF NOT EXISTS `comment`
(
    `comment_id`      int unsigned NOT NULL AUTO_INCREMENT,
    `comment_content` varchar(200) NOT NULL,

    PRIMARY KEY (`comment_id`)
);


-- ************************************** `character`

CREATE TABLE IF NOT EXISTS `character`
(
    `character_id`   int unsigned NOT NULL AUTO_INCREMENT,
    `character_name` varchar(50)  NOT NULL,

    PRIMARY KEY (`character_id`),
    UNIQUE KEY `name` (`character_name`)
);


-- ************************************** `episode_comment`

CREATE TABLE IF NOT EXISTS `episode_comment`
(
    `comment_id` int unsigned NOT NULL,
    `episode_id` int unsigned NOT NULL,

    PRIMARY KEY (`comment_id`),
    KEY `FK_ep_com_com` (`comment_id`),
    CONSTRAINT `FK_constr_ep_com_com` FOREIGN KEY `FK_ep_com_com` (`comment_id`) REFERENCES `comment` (`comment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    KEY `FK_ep_com_ep` (`episode_id`),
    CONSTRAINT `FK_constr_ep_com_ep` FOREIGN KEY `FK_ep_com_ep` (`episode_id`) REFERENCES `episode` (`episode_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ************************************** `episode_character_appearance`

CREATE TABLE IF NOT EXISTS `episode_character_appearance`
(
    `character` int unsigned NOT NULL,
    `episode`   int unsigned NOT NULL,

    PRIMARY KEY (`character`, `episode`),
    KEY `FK_ep_ap_char` (`character`),
    CONSTRAINT `FK_constr_episode_appearance_character` FOREIGN KEY `FK_ep_ap_char` (`character`) REFERENCES `character` (`character_id`) ON DELETE CASCADE ON UPDATE CASCADE,
    KEY `FK_ep_ap_ep` (`episode`),
    CONSTRAINT `FK_constr_episode_appearance_episode` FOREIGN KEY `FK_ep_ap_ep` (`episode`) REFERENCES `episode` (`episode_id`) ON DELETE CASCADE ON UPDATE CASCADE
);


-- ************************************** `character_comment`

CREATE TABLE IF NOT EXISTS `character_comment`
(
    `comment_id`   int unsigned NOT NULL,
    `character_id` int unsigned NOT NULL,

    PRIMARY KEY (`comment_id`),
    KEY `FK_char_com_char` (`comment_id`),
    CONSTRAINT `FK_constr_char_com_char` FOREIGN KEY `FK_char_com_char` (`comment_id`) REFERENCES `comment` (`comment_id`),
    KEY `FK_char_com_com` (`character_id`),
    CONSTRAINT `FK_constr_char_com_com` FOREIGN KEY `FK_char_com_com` (`character_id`) REFERENCES `character` (`character_id`)
);


-- ************************************** `episode_character_appearance_comment`

CREATE TABLE IF NOT EXISTS `episode_character_appearance_comment`
(
    `comment_id` int unsigned NOT NULL,
    `character`  int unsigned NOT NULL,
    `episode`    int unsigned NOT NULL,

    PRIMARY KEY (`comment_id`),
    KEY `FK_ep_char_ep_char` (`comment_id`),
    CONSTRAINT `FK_constr_ep_char_ep_char` FOREIGN KEY `FK_ep_char_ep_char` (`comment_id`) REFERENCES `comment` (`comment_id`),
    KEY `FK_ep_char_ep_com` (`character`, `episode`),
    CONSTRAINT `FK_constr_ep_char_ep_com` FOREIGN KEY `FK_ep_char_ep_com` (`character`, `episode`) REFERENCES `episode_character_appearance` (`character`, `episode`)
);



