-- ========================================[ Collection Tables ]========================================

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS `collection_decks`;
DROP TABLE IF EXISTS `collection_tags`;
DROP TABLE IF EXISTS `decks`;
DROP TABLE IF EXISTS `tags`;
DROP TABLE IF EXISTS `collection`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `languages`;
DROP TABLE IF EXISTS `rarities`;
DROP TABLE IF EXISTS `rarity_full_card_effects`;
DROP TABLE IF EXISTS `rarity_special_symbols`;
DROP TABLE IF EXISTS `rarity_card_image_effects`;
DROP TABLE IF EXISTS `rarity_card_name_effects`;

-- ======================================== Rarity Stuff ========================================

CREATE TABLE `rarity_card_name_effects` (
    `id` int NOT NULL,
    `name` varchar(255) NOT NULL,
    `description` text NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `rarity_card_image_effects` (
    `id` int NOT NULL,
    `name` varchar(255) NOT NULL,
    `description` text NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `rarity_special_symbols` (
    `id` int NOT NULL,
    `name` varchar(255) NOT NULL,
    `description` text NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `rarity_full_card_effects` (
    `id` int NOT NULL,
    `name` varchar(255) NOT NULL,
    `description` text NOT NULL,

    PRIMARY KEY (`id`)
);

CREATE TABLE `rarities` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(255) NOT NULL,
    `abbreviation` varchar(50) NOT NULL,
    `color_hex` varchar(7) NOT NULL,
    `card_name_effect_id` int DEFAULT NULL,
    `card_image_effect_id` int DEFAULT NULL,
    `special_symbol_id` int DEFAULT NULL,
    `full_card_effect_id` int DEFAULT NULL,
    `is_parallel` tinyint(1) NOT NULL DEFAULT 0,
    `is_promo` tinyint(1) NOT NULL DEFAULT 0,
    `is_embossed` tinyint(1) NOT NULL DEFAULT 0,
    `is_raised` tinyint(1) NOT NULL DEFAULT 0,
    `is_special_variant` tinyint(1) NOT NULL DEFAULT 0,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`card_name_effect_id`) REFERENCES `rarity_card_name_effects`(`id`),
    FOREIGN KEY (`card_image_effect_id`) REFERENCES `rarity_card_image_effects`(`id`),
    FOREIGN KEY (`full_card_effect_id`) REFERENCES `rarity_full_card_effects`(`id`),
    FOREIGN KEY (`special_symbol_id`) REFERENCES `rarity_special_symbols`(`id`)
);

-- ========== Card Name Effects ==========
INSERT IGNORE INTO `rarity_card_name_effects` (`id`, `name`, `description`) VALUES
    (1, 'Silver Foil', 'Card name is printed in silver foil.'),
    (2, 'Gold Foil', 'Card name is printed in gold foil.'),
    (3, 'Rainbow Foil', 'Card name uses rainbow/holographic foil.'),
    (4, 'Holo Foil', 'Card name uses generic holographic foil.'),
    (5, 'Colored Foil', 'Card name uses a colored foil (e.g., blue/green/purple).'),
    (6, 'Platinum Foil', 'Card name uses a platinum/silver-metallic foil.'),
    (7, 'Parallel Foil', 'Card name has a parallel foil treatment.');

-- ========== Card Image (Artwork) Effects ==========
INSERT IGNORE INTO `rarity_card_image_effects` (`id`, `name`, `description`) VALUES
    (1, 'Holo Foil', 'Artwork has standard holographic shine.'),
    (2, 'Prismatic / Starfoil', 'Artwork shows prismatic/star-like lattice or grid sparkle.'),
    (3, 'Parallel Foil Full', 'Parallel film/foil covers artwork (often the whole face).'),
    (4, 'Embossed / Raised', 'Artwork/borders are textured/raised.'),
    (5, 'Ghostly Foil', 'Pale, ghost-like holographic effect; image looks washed/3D.'),
    (6, 'Glitter / Confetti Foil', 'Sparkly dotted “confetti”/glitter appearance.');

-- ========== Full Card Effects ==========
INSERT IGNORE INTO `rarity_full_card_effects` (`id`, `name`, `description`) VALUES
    (1, 'Holo Overlay on Entire Card', 'Holographic sheen across most of the card face.'),
    (2, 'Prismatic Full', 'Prismatic/starfoil effect across most of the card face.'),
    (3, 'Parallel Full', 'Parallel film across most/all of the card face.'),
    (4, 'Embossed Full Card', 'Embossed/raised elements across borders/text boxes.'),
    (5, 'Border Foil', 'Prominent foil on the border/frame.'),
    (6, 'Hieroglyphic Overlay', 'Hieroglyphic/ancient-script overlay across the card.');

-- ========== Special Symbols / Stamps ==========
INSERT IGNORE INTO `rarity_special_symbols` (`id`, `name`, `description`) VALUES
    (1, '25th', 'Quarter Century (25th) stamp/watermark in the text box.'),
    (2, '20th', '20th Anniversary stamp/watermark in the text box (OCG).'),
    (3, 'Millennium Eye', 'Millennium Eye / hieroglyphic motif associated with Pharaoh’s/Millennium.'),
    (4, 'Set Logo Stamp', 'Set/collection logo printed in the text box.'),
    (5, 'Event Logo', 'Event/tournament prize stamp.'),
    (6, 'Anniversary Symbol', 'General anniversary stamp (non-20/25).'),
    (7, 'KC logo', 'Kaiba Corporation logo.'),
    (8, '10000 logo', '“10000” special stamp for 10, 000th card celebration.');

-- ==================== Rarities ====================
INSERT IGNORE INTO `rarities` (`id`, `name`, `abbreviation`, `color_hex`, `card_name_effect_id`, `card_image_effect_id`, `special_symbol_id`, `full_card_effect_id`, `is_parallel`, `is_promo`, `is_embossed`, `is_raised`, `is_special_variant`) VALUES
    -- ===== Core =====
    (1, 'Other', '-', '#000000', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0), -- fallback for unknown/unset rarity
    (2, 'Common', 'C', '#8f8f8f', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 0), -- no special treatment
    (3, 'Rare', 'R', '#2c4cff', 1, NULL, NULL, NULL, 0, 0, 0, 0, 0), -- silver foil name only
    (4, 'Super Rare', 'SR', '#ffd700', NULL, 1, NULL, NULL, 0, 0, 0, 0, 0), -- holo artwork only
    (5, 'Ultra Rare', 'UR', '#9d00ff', 2, 1, NULL, NULL, 0, 0, 0, 0, 0), -- gold foil name + holo artwork
    (6, 'Secret Rare', 'SCR', '#ff00ff', 2, 2, NULL, NULL, 0, 0, 0, 0, 0), -- gold foil name + prismatic artwork

    -- ===== Chase Types =====
    (7, 'Ultimate Rare', 'UTR', '#c090ff', 2, 4, NULL, 4, 0, 0, 1, 1, 1), -- gold foil name + embossed/raised full card
    (8, 'Ghost Rare', 'GR', '#f0f0f0', 1, 5, NULL, 1, 0, 0, 0, 0, 1), -- silver foil name + ghostly holo artwork
    (9, 'Collector\'s Rare', 'CR', '#80d0ff', 3, 4, NULL, 1, 0, 0, 1, 1, 1), -- rainbow foil name + embossed sparkle
    (10, 'Starlight Rare', 'StR', '#a0e0ff', 3, 2, NULL, 2, 0, 0, 0, 0, 1), -- rainbow foil name + prismatic full-card effect

    -- ===== Secret-variant families =====
    (11, 'Prismatic Secret Rare', 'PScR', '#a6a6ff', 1, 2, NULL, NULL, 0, 0, 0, 0, 1), -- silver foil name + prismatic artwork
    (12, 'Extra Secret Rare', 'EScR', '#ffa6ff', 3, 2, NULL, NULL, 0, 1, 0, 0, 1), -- rainbow foil name + prismatic artwork, promo
    (13, 'Secret Ultra Rare', 'ScUR', '#ffb380', 2, 2, NULL, NULL, 0, 1, 0, 0, 1), -- gold foil name + prismatic artwork, promo

    -- ===== Duel Terminal / Parallel (full-surface film) =====
    (14, 'Normal Parallel Rare (Duel Terminal)', 'NPR', '#b0e0e6', NULL, 3, NULL, 3, 1, 0, 0, 0, 1), -- common base + parallel film
    (15, 'Super Parallel Rare (Duel Terminal)', 'SPR', '#b0e0e6', NULL, 3, NULL, 3, 1, 0, 0, 0, 1), -- super base + parallel film
    (16, 'Ultra Parallel Rare (Duel Terminal)', 'UPR', '#b0e0e6', 2, 3, NULL, 3, 1, 0, 0, 0, 1), -- ultra base + parallel film
    (17, 'Secret Parallel Rare (Duel Terminal)', 'ScPR', '#b0e0e6', 3, 3, NULL, 3, 1, 0, 0, 0, 1), -- secret base + parallel film
    (18, 'Extra Secret Parallel Rare (Duel Terminal)', 'EScPR', '#b0e0e6', 3, 3, NULL, 3, 1, 0, 0, 0, 1), -- extra secret base + parallel film

    -- ===== Patterned “Battle Pack” style foils =====
    (19, 'Starfoil Rare', 'SFR', '#7fd7ff', NULL, 2, NULL, 2, 0, 0, 0, 0, 1), -- star-patterned prismatic foil
    (20, 'Mosaic Rare', 'MSR', '#7fd7ff', NULL, 2, NULL, 2, 0, 0, 0, 0, 1), -- mosaic blocky prismatic foil
    (21, 'Shatterfoil Rare', 'SHR', '#7fd7ff', NULL, 2, NULL, 2, 0, 0, 0, 0, 1), -- shatter-glass prismatic foil
    (22, 'Holofoil Rare', 'HFR', '#7fd7ff', NULL, 1, NULL, NULL, 0, 0, 0, 0, 1), -- holo artwork, variant naming

    -- ===== Gold / Platinum lines =====
    (23, 'Gold Rare', 'GUR', '#d4af37', 2, 1, NULL, 5, 0, 0, 0, 0, 1), -- gold name + holo art + border foil
    (24, 'Gold Secret Rare (Premium Gold)', 'GScR', '#d4af37', 2, 2, NULL, 5, 0, 0, 0, 0, 1), -- gold name + prismatic art + border foil
    (25, 'Premium Gold Rare', 'PGR', '#d4af37', 2, 1, NULL, 5, 0, 0, 1, 1, 1), -- gold name + thick embossed gold frame
    (26, 'Ghost/Gold Rare', 'GGR', '#d4af37', 2, 5, NULL, 5, 0, 0, 0, 0, 1), -- ghostly art + gold name/frame
    (27, 'Platinum Rare', 'PlR', '#c0c0c0', 6, 1, NULL, 5, 0, 0, 0, 0, 1), -- platinum name + holo art + border foil
    (28, 'Platinum Secret Rare', 'PlScR', '#c0c0c0', 3, 2, NULL, 2, 0, 1, 0, 0, 1), -- rainbow name + prismatic art + promo

    -- ===== OCG Holographic =====
    (29, 'Holographic Rare (OCG)', 'HR', '#e6e6e6', 1, 5, NULL, 1, 0, 0, 0, 0, 1), -- silver name + ghostly holo art
    (30, 'Holographic Parallel Rare (OCG)', 'HGPR', '#e6e6e6', 1, 3, NULL, 1, 1, 0, 0, 0, 1), -- silver name + ghostly parallel overlay

    -- ===== Millennium / Pharaoh’s style =====
    (31, 'Millennium Rare', 'MR', '#ccb28a', 2, 2, 3, 6, 0, 1, 0, 0, 1), -- gold name + prismatic art + Millennium Eye overlay
    (32, 'Ultra Rare (Pharaoh\'s Rare)', 'URP', '#ccb28a', 2, 2, 3, 6, 0, 1, 0, 0, 1), -- ultra base with hieroglyphic overlay

    -- ===== Anniversary / stamped variants =====
    (33, '20th Secret Rare (OCG)', '20ScR', '#ff99cc', 3, 2, 2, 2, 0, 1, 0, 0, 1), -- rainbow name + prismatic art + 20th stamp
    (34, 'Quarter Century Secret Rare', 'QCScR', '#ffcc66', 2, 2, 1, 2, 0, 1, 0, 0, 1), -- gold name + prismatic art + 25th stamp
    (35, '10000 Secret Rare', '10000ScR', '#ff6699', 3, 2, 8, 2, 0, 1, 0, 0, 1), -- rainbow name + prismatic art + 10000th stamp

    -- ===== Kaiba Corporation (KC) stamped =====
    (36, 'Kaiba Corporation Common', 'KCC', '#8f8f8f', NULL, NULL, 7, NULL, 0, 1, 0, 0, 1), -- common base + KC stamp
    (37, 'Kaiba Corporation Rare', 'KCR', '#2c4cff', 1, NULL, 7, NULL, 0, 1, 0, 0, 1), -- rare base + KC stamp
    (38, 'Kaiba Corporation Ultra Rare', 'KCUR', '#9d00ff', 2, 1, 7, NULL, 0, 1, 0, 0, 1), -- ultra base + KC stamp

    -- ===== Colored-name promos (Duelist League / Battle Pack variants) =====
    (39, 'Duelist League Rare (Blue Name)', 'DLR-B', '#4aa3ff', 5, NULL, 4, NULL, 0, 1, 0, 0, 1), -- colored foil name (blue) + set stamp
    (40, 'Duelist League Rare (Green Name)', 'DLR-G', '#56ff56', 5, NULL, 4, NULL, 0, 1, 0, 0, 1), -- colored foil name (green) + set stamp
    (41, 'Duelist League Rare (Purple Name)', 'DLR-P', '#b366ff', 5, NULL, 4, NULL, 0, 1, 0, 0, 1), -- colored foil name (purple) + set stamp

    -- ===== Generic catch-all parallel =====
    (42, 'Parallel Rare (catch-all)', 'PR', '#b0e0e6', NULL, 3, NULL, 3, 1, 0, 0, 0, 1), -- any base rarity + parallel film

    -- ===== Additional rarities =====
    (43, 'Normal Rare (OCG)', 'NR', '#8f8f8f', NULL, NULL, NULL, NULL, 0, 0, 0, 0, 1); -- OCG-only: printed as Common, distributed as Rare


-- ======================================== Language ========================================
CREATE TABLE `languages` (
    `id` int NOT NULL AUTO_INCREMENT,
    `name` varchar(100) NOT NULL,
    `abbreviation` varchar(10) NOT NULL,
    
    PRIMARY KEY (`id`)
);

INSERT IGNORE INTO `languages` (`name`, `abbreviation`) VALUES
    ('English', 'EN'),
    ('German', 'DE'),
    ('French', 'FR'),
    ('Italian', 'IT'),
    ('Spanish', 'SP'),
    ('Portuguese', 'PT'),
    ('Japanese', 'JP'),
    ('Korean', 'KR'),
    ('Chinese (Simplified)', 'SC'),
    ('Chinese (Traditional)', 'TC');


-- ======================================== Users ========================================
CREATE TABLE `users` (
    `id` int NOT NULL AUTO_INCREMENT,
    `username` varchar(255) NOT NULL UNIQUE,
    `password_hash` varchar(255) NOT NULL,
    `salt` varchar(255) NOT NULL,
    
    PRIMARY KEY (`id`),
    UNIQUE KEY `unique_username` (`username`)
);

-- ==================== Collection ====================
CREATE TABLE `collection` (
    `id` int NOT NULL AUTO_INCREMENT, -- collection entry id
    `user_id` int NOT NULL, -- the user this entry belongs to
    `card_id` int NOT NULL, -- the card this entry is for
    `set_id` int DEFAULT NULL, -- the set this card is from
    `rarity_id` int NOT NULL DEFAULT 1, -- the rarity of the card in this entry (default to 'Other')
    `language_id` int DEFAULT NULL, -- the language of the card in this entry
    `condition` int(100) DEFAULT NULL, -- condition of the card (0-100% or null if unknown)

    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
    FOREIGN KEY (`card_id`) REFERENCES `cards`(`id`),
    FOREIGN KEY (`rarity_id`) REFERENCES `rarities`(`id`),
    FOREIGN KEY (`language_id`) REFERENCES `languages`(`id`)
);

CREATE TABLE `tags` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `name` varchar(100) NOT NULL,
    `color_hex` varchar(7) NOT NULL,
    `description` text DEFAULT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `decks` (
    `id` int NOT NULL AUTO_INCREMENT,
    `user_id` int NOT NULL,
    `name` varchar(255) NOT NULL,
    `deck_color` varchar(7) NOT NULL,
    `description` text DEFAULT NULL,

    PRIMARY KEY (`id`),
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`)
);

CREATE TABLE `collection_tags` (
    `collection_id` int NOT NULL,
    `tag_id` int NOT NULL,

    PRIMARY KEY (`collection_id`, `tag_id`),
    FOREIGN KEY (`collection_id`) REFERENCES `collection`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`tag_id`) REFERENCES `tags`(`id`) ON DELETE CASCADE
);

CREATE TABLE `collection_decks` (
    `collection_id` int NOT NULL,
    `deck_id` int NOT NULL,
    `deck_section` enum('main','side','extra') NOT NULL DEFAULT 'main',

    PRIMARY KEY (`collection_id`, `deck_id`),
    FOREIGN KEY (`collection_id`) REFERENCES `collection`(`id`) ON DELETE CASCADE,
    FOREIGN KEY (`deck_id`) REFERENCES `decks`(`id`) ON DELETE CASCADE
);
