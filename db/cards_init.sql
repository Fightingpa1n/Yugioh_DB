-- all yugioh cards stuff

CREATE TABLE `cards` (
    `id` int NOT NULL AUTO_INCREMENT,
    `type_id` int,
    `name` varchar(255) NOT NULL,
    `description` text,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`type_id`) REFERENCES `card_types`(`id`)
);