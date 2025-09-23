
-- Drop existing tables if they exist
DROP TABLE IF EXISTS `user_cards`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `cards`;
DROP TABLE IF EXISTS `card_types`;

CREATE TABLE `card_types` (
    `id` int NOT NULL AUTO_INCREMENT,
    `type_name` varchar(100) NOT NULL,
    
    PRIMARY KEY (`id`)
);

INSERT INTO `card_types` (`id`, `type_name`) VALUES
    (1, 'Monster'),
    (2, 'Spell'),
    (3, 'Trap');

CREATE TABLE `cards` (
    `id` int NOT NULL AUTO_INCREMENT,
    `type_id` int,
    `name` varchar(255) NOT NULL,
    `description` text,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`type_id`) REFERENCES `card_types`(`id`)
);

CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    
    PRIMARY KEY (`id`)
);

CREATE TABLE `user_cards` (
    `user_id` int,
    `card_id` int,
    `quantity` int DEFAULT 1,
    
    PRIMARY KEY (`user_id`, `card_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`card_id`) REFERENCES `cards`(`id`)
);

