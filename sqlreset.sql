BEGIN;
ALTER TABLE `articles_articleaction_articles` DROP FOREIGN KEY `article_id_refs_id_f5ec1630`;
DROP TABLE `articles_article`;
DROP TABLE `articles_relationship`;
DROP TABLE `articles_articleaction_articles`;
DROP TABLE `articles_project`;
DROP TABLE `articles_articletype`;
DROP TABLE `articles_publishingoutletconfiguration`;
DROP TABLE `articles_publishingoutlet`;
DROP TABLE `articles_testoutlet`;
CREATE TABLE `articles_testoutlet` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `class_name` varchar(128) NOT NULL,
    `module_name` varchar(128) NOT NULL
)
;
CREATE TABLE `articles_publishingoutlet` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `class_name` varchar(128) NOT NULL,
    `module_name` varchar(128) NOT NULL,
    `title` varchar(256) NOT NULL
)
;
CREATE TABLE `articles_publishingoutletconfiguration` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL,
    `outlet_id` integer NOT NULL,
    `pickled_data` varchar(256) NOT NULL
)
;
ALTER TABLE `articles_publishingoutletconfiguration` ADD CONSTRAINT `outlet_id_refs_id_19563a40` FOREIGN KEY (`outlet_id`) REFERENCES `articles_publishingoutlet` (`id`);
ALTER TABLE `articles_publishingoutletconfiguration` ADD CONSTRAINT `user_id_refs_id_c92cbaf4` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `articles_articletype` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(16) NOT NULL
)
;
CREATE TABLE `articles_project` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(64) NOT NULL,
    `owner_id` integer NOT NULL
)
;
ALTER TABLE `articles_project` ADD CONSTRAINT `owner_id_refs_id_ebb294b5` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `articles_articleaction_articles` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `articleaction_id` integer NOT NULL,
    `article_id` integer NOT NULL,
    UNIQUE (`articleaction_id`, `article_id`)
)
;
CREATE TABLE `articles_articleaction` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `author_id` integer,
    `code` varchar(1) NOT NULL,
    `user_id` integer NOT NULL,
    `timestamp` datetime NOT NULL,
    `timezone` varchar(32) NOT NULL,
    `comment` varchar(64) NOT NULL
)
;
ALTER TABLE `articles_articleaction` ADD CONSTRAINT `author_id_refs_id_2ccd756a` FOREIGN KEY (`author_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `articles_articleaction` ADD CONSTRAINT `user_id_refs_id_2ccd756a` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `articles_articleaction_articles` ADD CONSTRAINT `articleaction_id_refs_id_3c95fe70` FOREIGN KEY (`articleaction_id`) REFERENCES `articles_articleaction` (`id`);
CREATE TABLE `articles_relationship` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `requester_id` integer NOT NULL,
    `writer_id` integer NOT NULL,
    `created_by_id` integer NOT NULL,
    `confirmed` bool NOT NULL
)
;
ALTER TABLE `articles_relationship` ADD CONSTRAINT `requester_id_refs_id_26e142d3` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `articles_relationship` ADD CONSTRAINT `writer_id_refs_id_26e142d3` FOREIGN KEY (`writer_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `articles_relationship` ADD CONSTRAINT `created_by_id_refs_id_26e142d3` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`);
CREATE TABLE `articles_article` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `minimum` integer NOT NULL,
    `maximum` integer NOT NULL,
    `body` longtext NOT NULL,
    `title` varchar(256) NOT NULL,
    `article_type_id` integer NOT NULL,
    `project_id` integer,
    `_tags` varchar(128) NOT NULL,
    `owner_id` integer NOT NULL,
    `expires` datetime,
    `last_action_id` integer,
    `published_id` integer,
    `approved_id` integer,
    `submitted_id` integer,
    `assigned_id` integer,
    `rejected_id` integer,
    `released_id` integer
)
;
ALTER TABLE `articles_article` ADD CONSTRAINT `last_action_id_refs_id_57ab54d7` FOREIGN KEY (`last_action_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `published_id_refs_id_57ab54d7` FOREIGN KEY (`published_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `approved_id_refs_id_57ab54d7` FOREIGN KEY (`approved_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `submitted_id_refs_id_57ab54d7` FOREIGN KEY (`submitted_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `assigned_id_refs_id_57ab54d7` FOREIGN KEY (`assigned_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `rejected_id_refs_id_57ab54d7` FOREIGN KEY (`rejected_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `released_id_refs_id_57ab54d7` FOREIGN KEY (`released_id`) REFERENCES `articles_articleaction` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `article_type_id_refs_id_d0b3bfad` FOREIGN KEY (`article_type_id`) REFERENCES `articles_articletype` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `project_id_refs_id_f35146a4` FOREIGN KEY (`project_id`) REFERENCES `articles_project` (`id`);
ALTER TABLE `articles_article` ADD CONSTRAINT `owner_id_refs_id_21e48f8a` FOREIGN KEY (`owner_id`) REFERENCES `auth_user` (`id`);
ALTER TABLE `articles_articleaction_articles` ADD CONSTRAINT `article_id_refs_id_f5ec1630` FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`);
CREATE TABLE `articles_keyword` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `article_id` integer NOT NULL,
    `keyword` varchar(32) NOT NULL,
    `url` varchar(64) NOT NULL,
    `times` integer NOT NULL
)
;
ALTER TABLE `articles_keyword` ADD CONSTRAINT `article_id_refs_id_210abd5c` FOREIGN KEY (`article_id`) REFERENCES `articles_article` (`id`);
CREATE TABLE `articles_userprofile` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `user_id` integer NOT NULL UNIQUE,
    `timezone` varchar(32) NOT NULL,
    `access_token` longtext,
    `preferred_mode` integer NOT NULL
)
;
ALTER TABLE `articles_userprofile` ADD CONSTRAINT `user_id_refs_id_895fd314` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
CREATE INDEX `articles_publishingoutletconfiguration_fbfc09f1` ON `articles_publishingoutletconfiguration` (`user_id`);
CREATE INDEX `articles_publishingoutletconfiguration_d46089b9` ON `articles_publishingoutletconfiguration` (`outlet_id`);
CREATE INDEX `articles_project_5d52dd10` ON `articles_project` (`owner_id`);
CREATE INDEX `articles_articleaction_cc846901` ON `articles_articleaction` (`author_id`);
CREATE INDEX `articles_articleaction_fbfc09f1` ON `articles_articleaction` (`user_id`);
CREATE INDEX `articles_relationship_b8ca8b9f` ON `articles_relationship` (`requester_id`);
CREATE INDEX `articles_relationship_62351b1d` ON `articles_relationship` (`writer_id`);
CREATE INDEX `articles_relationship_b5de30be` ON `articles_relationship` (`created_by_id`);
CREATE INDEX `articles_article_259c9845` ON `articles_article` (`article_type_id`);
CREATE INDEX `articles_article_b6620684` ON `articles_article` (`project_id`);
CREATE INDEX `articles_article_5d52dd10` ON `articles_article` (`owner_id`);
CREATE INDEX `articles_article_b1ef52ee` ON `articles_article` (`last_action_id`);
CREATE INDEX `articles_article_350cb3c1` ON `articles_article` (`published_id`);
CREATE INDEX `articles_article_a2a50e61` ON `articles_article` (`approved_id`);
CREATE INDEX `articles_article_bbbab57a` ON `articles_article` (`submitted_id`);
CREATE INDEX `articles_article_99f3e2b4` ON `articles_article` (`assigned_id`);
CREATE INDEX `articles_article_b4d16e8e` ON `articles_article` (`rejected_id`);
CREATE INDEX `articles_article_4d71038d` ON `articles_article` (`released_id`);
CREATE INDEX `articles_keyword_30525a19` ON `articles_keyword` (`article_id`);
COMMIT;
