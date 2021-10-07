CREATE TABLE `episode` (
  `episodeid` INT UNSIGNED NOT NULL auto_increment,
  `name` VARCHAR(200) NOT NULL,
  UNIQUE KEY `name` (`name`),
  PRIMARY KEY (`episodeid`)
) engine = innodb;

CREATE TABLE `character` (
  `characterid` INT UNSIGNED NOT NULL auto_increment,
  `name` VARCHAR(200) NOT NULL,
  UNIQUE KEY `name` (`name`),
  PRIMARY KEY (`characterid`)
) engine = innodb;

CREATE TABLE `episodeappearance` (
  `character` INT UNSIGNED NOT NULL,
  `episode` INT UNSIGNED NOT NULL,
  PRIMARY KEY (`character`, `episode`),
  CONSTRAINT `constr_episodeappearance_character_fk` FOREIGN KEY `character_fk` (`character`) REFERENCES `character` (`characterid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `constr_episodeappearance_episode_fk` FOREIGN KEY `episode_fk` (`episode`) REFERENCES `episode` (`episodeid`) ON DELETE CASCADE ON UPDATE CASCADE
) engine = innodb;