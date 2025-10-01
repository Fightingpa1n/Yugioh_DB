from flask import g
from util.db_connection import get_db

#======================================== Card Types Fetchers ========================================#
#==================== Card Types ====================#
def get_all_card_types() -> dict[int, str]:
    """Fetch all card types from the database."""
    if 'card_types' not in g:
        result = get_db().query("SELECT id, name FROM card_types")
        g.card_types = {row['id']: row['name'] for row in result} #type: ignore
    return g.card_types #type: ignore

#==================== Attributes ====================#
def get_all_attributes() -> dict[int, str]:
    """Fetch all attributes from the database."""
    if 'attributes' not in g:
        result = get_db().query("SELECT id, name FROM attributes")
        g.attributes = {row['id']: row['name'] for row in result} #type: ignore
    return g.attributes #type: ignore

#==================== Monster Types ====================#
def get_all_monster_types() -> dict[int, str]:
    """Fetch all monster types from the database."""
    if 'monster_types' not in g:
        result = get_db().query("SELECT id, name FROM monster_types")
        g.monster_types = {row['id']: row['name'] for row in result} #type: ignore
    return g.monster_types #type: ignore

#==================== Monster Subtypes ====================#
def get_all_monster_subtypes() -> dict[int, str]:
    """Fetch all monster subtypes from the database."""
    if 'monster_subtypes' not in g:
        result = get_db().query("SELECT id, name FROM monster_subtypes")
        g.monster_subtypes = {row['id']: row['name'] for row in result} #type: ignore
    return g.monster_subtypes #type: ignore

#==================== Spell/Trap Types ====================#
def get_all_spelltrap_types() -> dict[int, str]:
    """Fetch all spell/trap types from the database."""
    if 'spelltrap_types' not in g:
        result = get_db().query("SELECT id, name FROM spelltrap_types")
        g.spelltrap_types = {row['id']: row['name'] for row in result} #type: ignore
    return g.spelltrap_types #type: ignore


#======================================== Card Type Helpers ========================================#
#==================== Card Types ====================#
def get_card_type_id_by_name(name:str) -> int|None:
    """Get card type ID by name."""
    card_types = get_all_card_types()
    for type_id, type_name in card_types.items():
        if type_name.strip().lower() == name.strip().lower():
            return type_id
    return None

#==================== Attributes ====================#
def get_attribute_id_by_name(name:str) -> int|None:
    """Get attribute ID by name."""
    attributes = get_all_attributes()
    for attr_id, attr_name in attributes.items():
        if attr_name.strip().lower() == name.strip().lower():
            return attr_id
    return None

#==================== Monster Types ====================#
def get_monster_type_id_by_name(name:str) -> int|None:
    """Get monster type ID by name."""
    monster_types = get_all_monster_types()
    for type_id, type_name in monster_types.items():
        if type_name.strip().lower() == name.strip().lower():
            return type_id
    return None

#==================== Monster Subtypes ====================#
def get_monster_subtype_id_by_name(name:str) -> int|None:
    """Get monster subtype ID by name."""
    monster_subtypes = get_all_monster_subtypes()
    for subtype_id, subtype_name in monster_subtypes.items():
        if subtype_name.strip().lower() == name.strip().lower():
            return subtype_id
    return None

#==================== Spell/Trap Types ====================#
def get_spelltrap_type_id_by_name(name:str) -> int|None:
    """Get spell/trap type ID by name."""
    spelltrap_types = get_all_spelltrap_types()
    for type_id, type_name in spelltrap_types.items():
        if type_name.strip().lower() == name.strip().lower():
            return type_id
    return None
