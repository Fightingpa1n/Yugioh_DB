-- create tables for all cards and stuff

DROP TABLE IF EXISTS `sets`;
DROP TABLE IF EXISTS `cards`;
DROP TABLE IF EXISTS `card_types`;
DROP TABLE IF EXISTS `monster_subtypes`;
DROP TABLE IF EXISTS `attributes`;
DROP TABLE IF EXISTS `monster_types`;
DROP TABLE IF EXISTS `spelltrap_types`;

CREATE TABLE `card_types` ( -- e.g., Monster, Spell, Trap
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `monster_subtypes` ( -- e.g., Fusion, Synchro
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `attributes` ( -- e.g., Light, Dark, Earth
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `monster_types` ( -- e.g., Dragon, Warrior
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `spelltrap_types` ( -- e.g., Normal, Continuous
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `cards` ( -- main cards table
    `id` int NOT NULL, -- card id. (not auto Increment since we set manually)
    `type_id` int NOT NULL, -- foreign key to card_types
    `name` varchar(255) NOT NULL, -- card name
    `description` text NOT NULL, -- card description

    -- Spells/Traps
    `spelltrap_type_id` int DEFAULT NULL, -- foreign key to spelltrap_types (only for spells/traps)

    -- Monsters
    `attribute_id` int DEFAULT NULL, -- foreign key to attributes (only for monsters)
    `monster_type_id` int DEFAULT NULL, -- foreign key to monster_types (only for monsters)
    `monster_subtype_id` int DEFAULT NULL, -- foreign key to monster_subtypes (only for monsters)
    `level` int DEFAULT NULL, -- monster level/ranked (only for monsters)
    `attack` int DEFAULT NULL, -- monster attack points (only for monsters)
    `defense` int DEFAULT NULL, -- monster defense points (only for monsters)
    `is_effect` tinyint(1) DEFAULT NULL, -- is it an effect monster? (only for monsters)
    `is_tuner` tinyint(1) DEFAULT NULL, -- is it a tuner monster? (only for monsters)

    -- Link
    `link_rating` int DEFAULT NULL, -- link rating (only for link monsters)
    `link_arrow_top_right` tinyint(1) DEFAULT NULL, -- link arrow top right (only for link monsters)
    `link_arrow_top_center` tinyint(1) DEFAULT NULL, -- link arrow top center (only for link monsters)
    `link_arrow_top_left` tinyint(1) DEFAULT NULL, -- link arrow top left (only for link monsters)
    `link_arrow_middle_right` tinyint(1) DEFAULT NULL, -- link arrow middle right (only for link monsters)
    `link_arrow_middle_left` tinyint(1) DEFAULT NULL, -- link arrow middle left (only for link monsters)
    `link_arrow_bottom_right` tinyint(1) DEFAULT NULL, -- link arrow bottom right (only for link monsters)
    `link_arrow_bottom_center` tinyint(1) DEFAULT NULL, -- link arrow bottom center (only for link monsters)
    `link_arrow_bottom_left` tinyint(1) DEFAULT NULL, -- link arrow bottom left (only for link monsters)

    -- Pendulum
    `pendulum_effect` text DEFAULT NULL, -- pendulum effect (only for pendulum monsters)
    `pendulum_scale` int DEFAULT NULL, -- pendulum scale (only for pendulum monsters)

    -- Skill cards
    `skill_owner` varchar(100) DEFAULT NULL, -- owner of the skill card (only for skill cards)

    PRIMARY KEY (`id`),
    FOREIGN KEY (`type_id`) REFERENCES `card_types`(`id`),
    FOREIGN KEY (`spelltrap_type_id`) REFERENCES `spelltrap_types`(`id`),
    FOREIGN KEY (`attribute_id`) REFERENCES `attributes`(`id`),
    FOREIGN KEY (`monster_type_id`) REFERENCES `monster_types`(`id`),
    FOREIGN KEY (`monster_subtype_id`) REFERENCES `monster_subtypes`(`id`)
);

CREATE TABLE `sets` ( -- yugioh card sets
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL, -- set name
    `code` varchar(50) NOT NULL, -- set code

    PRIMARY KEY (`id`)
);


-- insert some initial data

INSERT INTO `card_types` (`id`, `name`) VALUES -- card types
    (1, 'Monster'),
    (2, 'Spell'),
    (3, 'Trap'),
    (4, 'Token'),
    (5, 'Skill');

INSERT INTO `monster_subtypes` (`id`, `name`) VALUES -- monster subtypes
    (1, 'Normal'),
    (2, 'Fusion'),
    (3, 'Ritual'),
    (4, 'Synchro'),
    (5, 'Xyz'),
    (6, 'Link'),
    (7, 'Pendulum');

INSERT INTO `attributes` (`id`, `name`) VALUES -- monster attributes
    (1, 'Light'),
    (2, 'Dark'),
    (3, 'Earth'),
    (4, 'Water'),
    (5, 'Fire'),
    (6, 'Wind'),
    (7, 'Divine');

INSERT INTO `monster_types` (`id`, `name`) VALUES -- monster types
    (1, 'Aqua'),
    (2, 'Beast'),
    (3, 'Beast-Warrior'),
    (4, 'Creator God'),
    (5, 'Cyberse'),
    (6, 'Dinosaur'),
    (7, 'Divine-Beast'),
    (8, 'Dragon'),
    (9, 'Fairy'),
    (10, 'Fiend'),
    (11, 'Fish'),
    (12, 'Insect'),
    (13, 'Illusion'),
    (14, 'Machine'),
    (15, 'Plant'),
    (16, 'Psychic'),
    (17, 'Pyro'),
    (18, 'Reptile'),
    (19, 'Rock'),
    (20, 'Sea Serpent'),
    (21, 'Spellcaster'),
    (22, 'Thunder'),
    (23, 'Warrior'),
    (24, 'Winged Beast'),
    (25, 'Wyrm'),
    (26, 'Zombie');

INSERT INTO `spelltrap_types` (`id`, `name`) VALUES -- spell/trap types
    (1, 'Normal'),
    (2, 'Continuous'),
    (3, 'Equip'),
    (4, 'Field'),
    (5, 'Quick-Play'),
    (6, 'Ritual'),
    (7, 'Counter');