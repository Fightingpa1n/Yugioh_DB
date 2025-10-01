-- create tables for all cards and stuff

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
    `image` varchar(255) DEFAULT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `monster_types` ( -- e.g., Dragon, Warrior
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `image` varchar(255) DEFAULT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `spelltrap_types` ( -- e.g., Normal, Continuous
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `image` varchar(255) DEFAULT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `cards` ( -- main cards table
    `id` int NOT NULL, -- card id. (not auto Increment since we set manually)
    `type_id` int NOT NULL, -- foreign key to card_types
    `name` varchar(255) NOT NULL, -- card name
    `description` text NOT NULL, -- card description
    `image` varchar(255) DEFAULT NULL, -- card image filename
    `small_image` varchar(255) DEFAULT NULL, -- small card image filename
    `lookup_url` varchar(255) DEFAULT NULL, -- url to lookup more info about the card

    -- Spells/Traps
    `spelltrap_type_id` int DEFAULT NULL, -- foreign key to spelltrap_types (only for spells/traps)

    -- Monsters
    `attribute_id` int DEFAULT NULL, -- foreign key to attributes (only for monsters)
    `monster_type_id` int DEFAULT NULL, -- foreign key to monster_types (only for monsters)
    `level` int DEFAULT NULL, -- monster level/ranked (only for monsters)
    `attack` int DEFAULT NULL, -- monster attack points (only for monsters)
    `defense` int DEFAULT NULL, -- monster defense points (only for monsters)

    -- Link
    `link_rating` int DEFAULT NULL, -- link rating (only for link monsters)
    `link_arrow_top_left` tinyint(1) DEFAULT NULL, -- link arrow top left (only for link monsters)
    `link_arrow_top_center` tinyint(1) DEFAULT NULL, -- link arrow top center (only for link monsters)
    `link_arrow_top_right` tinyint(1) DEFAULT NULL, -- link arrow top right (only for link monsters)
    `link_arrow_middle_left` tinyint(1) DEFAULT NULL, -- link arrow middle left (only for link monsters)
    `link_arrow_middle_right` tinyint(1) DEFAULT NULL, -- link arrow middle right (only for link monsters)
    `link_arrow_bottom_left` tinyint(1) DEFAULT NULL, -- link arrow bottom left (only for link monsters)
    `link_arrow_bottom_center` tinyint(1) DEFAULT NULL, -- link arrow bottom center (only for link monsters)
    `link_arrow_bottom_right` tinyint(1) DEFAULT NULL, -- link arrow bottom right (only for link monsters)

    -- Pendulum
    `pendulum_effect` text DEFAULT NULL, -- pendulum effect (only for pendulum monsters)
    `pendulum_scale` int DEFAULT NULL, -- pendulum scale (only for pendulum monsters)

    -- Skill cards
    `skill_owner` varchar(100) DEFAULT NULL, -- owner of the skill card (only for skill cards)

    PRIMARY KEY (`id`),
    FOREIGN KEY (`type_id`) REFERENCES `card_types`(`id`),
    FOREIGN KEY (`spelltrap_type_id`) REFERENCES `spelltrap_types`(`id`),
    FOREIGN KEY (`attribute_id`) REFERENCES `attributes`(`id`),
    FOREIGN KEY (`monster_type_id`) REFERENCES `monster_types`(`id`)
);

CREATE TABLE `monsters_subtypes_junction` (
    `card_id` int NOT NULL,
    `monster_subtype_id` int NOT NULL,
    
    PRIMARY KEY (`card_id`, `monster_subtype_id`),
    FOREIGN KEY (`card_id`) REFERENCES `cards`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`monster_subtype_id`) REFERENCES `monster_subtypes`(`id`) ON DELETE CASCADE
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
    (2, 'Effect'),
    (3, 'Fusion'),
    (4, 'Ritual'),
    (5, 'Synchro'),
    (6, 'Xyz'),
    (7, 'Link'),
    (8, 'Pendulum'),
    (9, 'Gemini'),
    (10, 'Spirit'),
    (11, 'Toon'),
    (12, 'Union'),
    (13, 'Tuner'),
    (14, 'Flip');

INSERT INTO `attributes` (`id`, `name`, `image`) VALUES -- monster attributes
    (1, 'Light', 'assets/attributes/light.png'),
    (2, 'Dark', 'assets/attributes/dark.png'),
    (3, 'Earth', 'assets/attributes/earth.png'),
    (4, 'Water', 'assets/attributes/water.png'),
    (5, 'Fire', 'assets/attributes/fire.png'),
    (6, 'Wind', 'assets/attributes/wind.png'),
    (7, 'Divine', 'assets/attributes/divine.png');

INSERT INTO `monster_types` (`id`, `name`, `image`) VALUES -- monster types
    (1, 'Aqua', 'assets/monster_types/aqua.png'),
    (2, 'Beast', 'assets/monster_types/beast.png'),
    (3, 'Beast-Warrior', 'assets/monster_types/beast_warrior.png'),
    (4, 'Creator God', 'assets/monster_types/creator_god.png'),
    (5, 'Cyberse', 'assets/monster_types/cyberse.png'),
    (6, 'Dinosaur', 'assets/monster_types/dinosaur.png'),
    (7, 'Divine-Beast', 'assets/monster_types/divine_beast.png'),
    (8, 'Dragon', 'assets/monster_types/dragon.png'),
    (9, 'Fairy', 'assets/monster_types/fairy.png'),
    (10, 'Fiend', 'assets/monster_types/fiend.png'),
    (11, 'Fish', 'assets/monster_types/fish.png'),
    (12, 'Insect', 'assets/monster_types/insect.png'),
    (13, 'Illusion', 'assets/monster_types/illusion.png'),
    (14, 'Machine', 'assets/monster_types/machine.png'),
    (15, 'Plant', 'assets/monster_types/plant.png'),
    (16, 'Psychic', 'assets/monster_types/psychic.png'),
    (17, 'Pyro', 'assets/monster_types/pyro.png'),
    (18, 'Reptile', 'assets/monster_types/reptile.png'),
    (19, 'Rock', 'assets/monster_types/rock.png'),
    (20, 'Sea Serpent', 'assets/monster_types/sea_serpent.png'),
    (21, 'Spellcaster', 'assets/monster_types/spellcaster.png'),
    (22, 'Thunder', 'assets/monster_types/thunder.png'),
    (23, 'Warrior', 'assets/monster_types/warrior.png'),
    (24, 'Winged Beast', 'assets/monster_types/winged_beast.png'),
    (25, 'Wyrm', 'assets/monster_types/wyrm.png'),
    (26, 'Zombie', 'assets/monster_types/zombie.png');

INSERT INTO `spelltrap_types` (`id`, `name`, `image`) VALUES -- spell/trap types
    (1, 'Normal', NULL),
    (2, 'Continuous', 'assets/spelltrap_types/continuous.png'),
    (3, 'Equip', 'assets/spelltrap_types/equip.png'),
    (4, 'Field', 'assets/spelltrap_types/field.png'),
    (5, 'Quick-Play', 'assets/spelltrap_types/quick_play.png'),
    (6, 'Ritual', 'assets/spelltrap_types/ritual.png'),
    (7, 'Counter', 'assets/spelltrap_types/counter.png');