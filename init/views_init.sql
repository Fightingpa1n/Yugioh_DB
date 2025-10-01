-- Views for easier data retrieval

-- ======================================== All Cards ========================================
-- all cards
CREATE VIEW `all_cards` AS
SELECT
    `c`.`id` AS `id`,
    `c`.`type_id` AS `card_type_id`,
    `ct`.`name` AS `card_type`,
    `c`.`name` AS `name`,
    `c`.`description` AS `description`,
    `c`.`image` AS `image`,
    `c`.`small_image` AS `small_image`,
    `c`.`lookup_url` AS `lookup_url`,
    `att`.`id` AS `attribute_id`,
    `att`.`name` AS `attribute`,
    `att`.`image` AS `attribute_image`,
    `stt`.`id` AS `spelltrap_type_id`,
    `stt`.`name` AS `spelltrap_type`,
    `stt`.`image` AS `spelltrap_type_image`,
    `mt`.`id` AS `monster_type_id`,
    `mt`.`name` AS `monster_type`,
    `mt`.`image` AS `monster_type_image`,
    GROUP_CONCAT(DISTINCT `mst`.`name` ORDER BY `mst`.`name` SEPARATOR ', ') AS `monster_subtypes`,
    `c`.`level` AS `level`,
    `c`.`attack` AS `attack`,
    `c`.`defense` AS `defense`,
    `c`.`link_rating` AS `link_rating`,
    `c`.`link_arrow_top_left` AS `link_arrow_top_left`,
    `c`.`link_arrow_top_center` AS `link_arrow_top_center`,
    `c`.`link_arrow_top_right` AS `link_arrow_top_right`,
    `c`.`link_arrow_middle_left` AS `link_arrow_middle_left`,
    `c`.`link_arrow_middle_right` AS `link_arrow_middle_right`,
    `c`.`link_arrow_bottom_left` AS `link_arrow_bottom_left`,
    `c`.`link_arrow_bottom_center` AS `link_arrow_bottom_center`,
    `c`.`link_arrow_bottom_right` AS `link_arrow_bottom_right`,
    `c`.`pendulum_scale` AS `pendulum_scale`,
    `c`.`pendulum_effect` AS `pendulum_effect`,
    `c`.`skill_owner` AS `skill_owner`
FROM `cards` `c`
LEFT JOIN `card_types` `ct` ON `c`.`type_id` = `ct`.`id`
LEFT JOIN `spelltrap_types` `stt` ON `c`.`spelltrap_type_id` = `stt`.`id`
LEFT JOIN `attributes` `att` ON `c`.`attribute_id` = `att`.`id`
LEFT JOIN `monster_types` `mt` ON `c`.`monster_type_id` = `mt`.`id`
LEFT JOIN `monsters_subtypes_junction` `mstj` ON `c`.`id` = `mstj`.`card_id`
LEFT JOIN `monster_subtypes` `mst` ON `mstj`.`monster_subtype_id` = `mst`.`id`
GROUP BY `c`.`id`, `c`.`type_id`, `ct`.`name`, `c`.`name`, `c`.`description`, `c`.`image`, 
         `c`.`small_image`, `c`.`lookup_url`, `att`.`id`, `att`.`name`, `att`.`image`,
         `stt`.`id`, `stt`.`name`, `stt`.`image`, `mt`.`id`, `mt`.`name`, `mt`.`image`,
         `c`.`level`, `c`.`attack`, `c`.`defense`, `c`.`link_rating`, `c`.`link_arrow_top_left`,
         `c`.`link_arrow_top_center`, `c`.`link_arrow_top_right`, `c`.`link_arrow_middle_left`,
         `c`.`link_arrow_middle_right`, `c`.`link_arrow_bottom_left`, `c`.`link_arrow_bottom_center`,
         `c`.`link_arrow_bottom_right`, `c`.`pendulum_scale`, `c`.`pendulum_effect`, `c`.`skill_owner`;

-- all monsters
CREATE VIEW `all_monsters` AS
SELECT
    `id`,
    `name`,
    `description`,
    `attribute_id`,
    `attribute`,
    `attribute_image`,
    `monster_type_id`,
    `monster_type`,
    `monster_type_image`,
    `monster_subtypes`,
    `level`,
    `attack`,
    `defense`,
    `link_rating`,
    `link_arrow_top_left`,
    `link_arrow_top_center`,
    `link_arrow_top_right`,
    `link_arrow_middle_left`,
    `link_arrow_middle_right`,
    `link_arrow_bottom_left`,
    `link_arrow_bottom_center`,
    `link_arrow_bottom_right`,
    `pendulum_scale`,
    `pendulum_effect`,
    `image`,
    `small_image`,
    `lookup_url`
FROM `all_cards`
WHERE `card_type_id` = 1; -- Monster id is 1

-- all spells
CREATE VIEW `all_spells` AS
SELECT
    `id`,
    `name`,
    `description`,
    `spelltrap_type_id` AS `spell_type_id`,
    `spelltrap_type` AS `spell_type`,
    `spelltrap_type_image` AS `spell_type_image`,
    `image`,
    `small_image`,
    `lookup_url`
FROM `all_cards`
WHERE `card_type_id` = 2; -- Spell id is 2

-- all traps
CREATE VIEW `all_traps` AS
SELECT
    `id`,
    `name`,
    `description`,
    `spelltrap_type` AS `trap_type`,
    `spelltrap_type_id` AS `trap_type_id`,
    `spelltrap_type_image` AS `trap_type_image`,
    `image`,
    `small_image`,
    `lookup_url`
FROM `all_cards`
WHERE `card_type_id` = 3; -- Trap id is 3

-- all tokens
CREATE VIEW `all_tokens` AS
SELECT
    `id`,
    `name`,
    `description`,
    `image`,
    `small_image`,
    `lookup_url`
FROM `all_cards`
WHERE `card_type_id` = 4; -- Token id is 4

-- skill cards
CREATE VIEW `all_skill_cards` AS
SELECT
    `id`,
    `name`,
    `description`,
    `skill_owner`,
    `image`,
    `small_image`,
    `lookup_url`
FROM `all_cards`
WHERE `card_type_id` = 5; -- Skill id is 5

-- TODO: add views for user collection stuff
-- ======================================== User Collection ========================================
-- CREATE VIEW `user_collection` AS
-- SELECT
--     `uc`.`id` AS `collection_entry`,
    
--     `u`.`id` AS `user_id`,
--     `u`.`username` AS `username`,

--     `c`.`id` AS `card_id`,
--     `c`.`card_type_id` AS `card_type_id`,
--     `c`.`card_type` AS `card_type`,
--     `c`.`name` AS `card_name`,
--     `c`.`description` AS `card_description`,
--     `c`.`image` AS `card_image`,
--     `c`.`lookup_url` AS `card_lookup_url`,
--     `c`.`attribute_id` AS `attribute_id`,
--     `c`.`attribute` AS `attribute`,
--     `c`.`attribute_image` AS `attribute_image`,
--     `c`.`spelltrap_type_id` AS `spelltrap_type_id`,
--     `c`.`spelltrap_type` AS `spelltrap_type`,
--     `c`.`spelltrap_type_image` AS `spelltrap_type_image`,
--     `c`.`monster_type_id` AS `monster_type_id`,
--     `c`.`monster_type` AS `monster_type`,
--     `c`.`monster_type_image` AS `monster_type_image`,
--     `c`.`monster_subtype_id` AS `monster_subtype_id`,
--     `c`.`monster_subtype` AS `monster_subtype`,
--     `c`.`level` AS `level`,
--     `c`.`attack` AS `attack`,
--     `c`.`defense` AS `defense`,
--     `c`.`is_effect` AS `is_effect`,
--     `c`.`is_tuner` AS `is_tuner`,
--     `c`.`link_rating` AS `link_rating`,
--     `c`.`link_arrow_top_right` AS `link_arrow_top_right`,
--     `c`.`link_arrow_top_center` AS `link_arrow_top_center`,
--     `c`.`link_arrow_top_left` AS `link_arrow_top_left`,
--     `c`.`link_arrow_middle_right` AS `link_arrow_middle_right`,
--     `c`.`link_arrow_middle_left` AS `link_arrow_middle_left`,
--     `c`.`link_arrow_bottom_right` AS `link_arrow_bottom_right`,
--     `c`.`link_arrow_bottom_center` AS `link_arrow_bottom_center`,
--     `c`.`link_arrow_bottom_left` AS `link_arrow_bottom_left`,
--     `c`.`link_arrow_bottom_right` AS `link_arrow_bottom_right`,
--     `c`.`pendulum_scale` AS `pendulum_scale`,
--     `c`.`pendulum_effect` AS `pendulum_effect`,
--     `c`.`skill_owner` AS `skill_owner`
    
--     `s`.`id` AS `set_id`,
--     `s`.`name` AS `set_name`,

--     `uc`.`card_number` AS `card_number`,
--     `l`.`id` AS `language_id`,
--     `l`.`name` AS `language`,

--     CONCAT(`s`.`code`, '-', `l`.`code`, `uc`.`card_number`) AS `full_card_code`,
--     `r`.`id` AS `rarity_id`,
--     `r`.`name` AS `rarity_name`,
--     `r`.`abreviation` AS `rarity`,
--     `r`.`color` AS `rarity_color`,

    

    





-- FROM `collection` `uc`
-- LEFT JOIN `users` `u` ON `uc`.`user_id` = `u`.`id`
-- LEFT JOIN `all_cards` `c` ON `uc`.`card_id` = `c`.`id`;
