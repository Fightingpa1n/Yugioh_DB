from util.db_connection import get_db
from util.data_handling import download_image, boolean_to_int
from modules.cards.types import get_card_type_id_by_name, get_attribute_id_by_name, get_monster_type_id_by_name, get_monster_subtype_id_by_name


#======================================== Helpers ========================================#
def link_markers_dict(link_markers:dict[str, bool]|None=None) -> dict[str, bool]:
    default_markers = {
        'top_left': False,
        'top_center': False,
        'top_right': False,
        'middle_left': False,
        'middle_right': False,
        'bottom_left': False,
        'bottom_center': False,
        'bottom_right': False,
    }

    if link_markers is None: return default_markers
    default_markers.update(link_markers)
    return default_markers.copy()

def extract_types(types:list[str]) -> tuple[str|None, list[str]]:
    """Extract monster type and subtype from a list of types."""

    #Example = ['Warrior', 'Effect']
    monster_type = None
    monster_subtypes = []

    for type_name in types:
        type_id = get_monster_type_id_by_name(type_name)
        if type_id:
            monster_type = type_name
            continue

        subtype_id = get_monster_subtype_id_by_name(type_name)
        if subtype_id: #if it's a valid subtype
            monster_subtypes.append(type_name)
            continue
    
    return monster_type, monster_subtypes


#======================================== Monsters ========================================#
def add(id:int, name:str, description:str, image_url:str, small_image_url:str, lookup_url:str, attribute:str, level:int|None, types:list[str], attack:int, defense:int|None, link_markers:dict[str, bool]|None, link_value:int|None=None, pendulum_scale:int|None=None, pendulum_effect:str|None=None):
    """ Add a monster card to the database.
        - id(int): The unique ID of the card.
        - name(str): The name of the card.
        - description(str): The card's description or effect text.
        - image_url(str): URL to the card's main image.
        - small_image_url(str): URL to the card's small image.
        - lookup_url(str): URL to the card's page on YGOProDeck.
        - attribute(str): The card's attribute (e.g., "DARK", "LIGHT").
        - level(int): The card's level
        - types(list[str]): List of the card's types (e.g., ["Dragon", "Effect"]).
        - attack(int): The card's attack points.
        - defense(int): The card's defense points.
        - link_markers(list[str]): List of the card's link markers (if it's a Link Monster).
        - link_value(int|None): The card's link value (if it's a Link Monster).
        - pendulum_scale(int|None): The card's pendulum scale (if it's a Pendulum Monster).
        - pendulum_effect(str|None): The card's pendulum effect (if it's a Pendulum Monster).
    """
    try:
        image_name = f"{id}.jpg"
        image_path = f"assets/card_images/monsters/{image_name}"
        small_image_path = f"assets/small_card_images/monsters/{image_name}"

        download_image(image_url, image_path)
        download_image(small_image_url, small_image_path)

        monster_type, monster_subtypes = extract_types(types)
        
        if not (monster_type):
            print(f"Warning: Could not determine monster type for card '{name}' (ID: {id}). Types provided: {types}")
            return
        
        link_markers = link_markers_dict(link_markers)

        get_db().execute(
            """
            INSERT IGNORE INTO `cards` (
                `id`, `type_id`, `name`, `description`,
                `image`, `small_image`, `lookup_url`,
                `attribute_id`, `monster_type_id`,
                `level`, `attack`, `defense`,
                `link_rating`,
                `link_arrow_top_left`, `link_arrow_top_center`, `link_arrow_top_right`,
                `link_arrow_middle_left`, `link_arrow_middle_right`,
                `link_arrow_bottom_left`, `link_arrow_bottom_center`, `link_arrow_bottom_right`,
                `pendulum_scale`, `pendulum_effect`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                id,
                get_card_type_id_by_name("Monster"),
                name, description,
                image_path, small_image_path, lookup_url,
                get_attribute_id_by_name(attribute) if attribute else None,
                get_monster_type_id_by_name(monster_type) if monster_type else None,
                level if level else None,
                attack if attack else None,
                defense if defense else None,
                link_value if link_value else None,
                boolean_to_int(link_markers.get('top_left', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('top_center', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('top_right', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('middle_left', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('middle_right', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('bottom_left', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('bottom_center', False)) if (link_value and link_markers) else None, #type: ignore
                boolean_to_int(link_markers.get('bottom_right', False)) if (link_value and link_markers) else None, #type: ignore
                pendulum_scale if pendulum_scale else None,
                pendulum_effect if pendulum_effect else None
            )
        )

        #Insert monster subtypes into the junction table
        query = "INSERT IGNORE INTO `monsters_subtypes_junction` (`card_id`, `monster_subtype_id`) VALUES "
        values = ()
        for subtype in monster_subtypes:
            subtype_id = get_monster_subtype_id_by_name(subtype)
            if subtype_id:
                query += "(%s, %s),"
                values += (id, subtype_id)
        if values:
            query = query.rstrip(',')  #Remove trailing comma
            get_db().execute(query, values)
    except Exception as e:
        print(f"Error adding monster card: {e}")
