import requests
import json

API_URL = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

#======================================== Helpers ========================================#
def update_sets(card_sets:list[dict], all_sets:list[dict]) -> list[dict]:
    """Updates the list of all card sets with the new card sets."""
    existing_set_names = {s['set_name'] for s in all_sets}
    for card_set in card_sets:
        if card_set['set_name'] not in existing_set_names:
            all_sets.append({
                'set_name': card_set['set_name'],
                'set_code': card_set['set_code'].split('-')[0], #only keep the first part of the set code (second part is card specific)
            })
            existing_set_names.add(card_set['set_name'])
    return all_sets

def format_card(card_data) -> tuple[str, dict]:
    """Formats the card data into a more structured dictionary."""
    if 'Monster' in card_data.get('type', ""):
        card = format_monster_card(card_data)
        card_type = "monster"
    elif 'Spell' in card_data.get('type', ''):
        card = format_spelltrap_card(card_data)
        card_type = "spell"
    elif 'Trap' in card_data.get('type', ''):
        card = format_spelltrap_card(card_data)
        card_type = "trap"
    elif 'Token' in card_data.get('type', ''):
        card = format_token_card(card_data)
        card_type = "token"
    elif 'Skill Card' in card_data.get('type', ''):
        card = format_skill_card(card_data)
        card_type = "skill"
    else:
        card = card_data
        card_type = "other"
    return card_type, card

def format_monster_card(card_data) -> dict:
    """Formats monster card data."""
    pendulum_effect, monster_effect = _split_description(card_data.get('desc', ""))
    images = card_data.get('card_images', [])
    image_url = images[0]['image_url'] if images else None
    image_url_small = images[0]['image_url_small'] if images else None
    card = {
        'id': card_data.get('id'),
        'name': card_data.get('name'),
        "description": monster_effect,
        'type': card_data.get('type', None),
        'types': card_data.get('typeline', []),
        'atk': card_data.get('atk', None),
        'def': card_data.get('def', None),
        'level': card_data.get('level', None),
        'attribute': card_data.get('attribute', None),
        'link_value': card_data.get('linkval', None),
        'link_markers': _get_link_markers(card_data.get('linkmarkers', [])),
        'pendulum_scale': card_data.get('scale', None),
        'pendulum_effect': pendulum_effect,
        'image_url': image_url,
        'image_url_small': image_url_small,
        'api_url': card_data.get('ygoprodeck_url', None)
    }
    return card

def format_spelltrap_card(card_data) -> dict:
    """Formats spell/trap card data."""
    images = card_data.get('card_images', [])
    image_url = images[0]['image_url'] if images else None
    image_url_small = images[0]['image_url_small'] if images else None
    card = {
        'id': card_data.get('id'),
        'name': card_data.get('name'),
        'description': card_data.get('desc', ''),
        'type': card_data.get('race', None),
        'image_url': image_url,
        'image_url_small': image_url_small,
        'api_url': card_data.get('ygoprodeck_url', None)
    }
    return card

def format_token_card(card_data) -> dict:
    """Formats token card data."""
    images = card_data.get('card_images', [])
    image_url = images[0]['image_url'] if images else None
    image_url_small = images[0]['image_url_small'] if images else None
    card = {
        'id': card_data.get('id'),
        'name': card_data.get('name'),
        'description': card_data.get('desc', ''),
        'image_url': image_url,
        'image_url_small': image_url_small,
        'api_url': card_data.get('ygoprodeck_url', None)
    }
    return card

def format_skill_card(card_data) -> dict:
    """Formats skill card data."""
    images = card_data.get('card_images', [])
    image_url = images[0]['image_url'] if images else None
    image_url_small = images[0]['image_url_small'] if images else None
    card = {
        'id': card_data.get('id'),
        'name': card_data.get('name'),
        'description': card_data.get('desc', ''),
        'skill_owner': card_data.get('race', None), #race field is used for skill owner
        'image_url': image_url,
        'image_url_small': image_url_small,
        'api_url': card_data.get('ygoprodeck_url', None)
    }
    return card

#==================== Helper Helpers ====================#
def _get_link_markers(link_markers:list[str]) -> dict[str, bool]:
    """Converts link markers list to a dictionary of boolean values."""
    markers = {}
    markers['top_left'] = 'Top-Left' in link_markers
    markers['top_center'] = 'Top-Center' in link_markers
    markers['top_right'] = 'Top-Right' in link_markers
    markers['middle_left'] = 'Middle-Left' in link_markers
    markers['middle_right'] = 'Middle-Right' in link_markers
    markers['bottom_left'] = 'Bottom-Left' in link_markers
    markers['bottom_center'] = 'Bottom-Center' in link_markers
    markers['bottom_right'] = 'Bottom-Right' in link_markers
    return markers

def _split_description(desc) -> tuple[str|None, str]:
    """Splits the description into pendulum and monster effects if applicable."""
    pendulum_indicator = "[ Pendulum Effect ]"
    monster_indicator = "[ Monster Effect ]"

    if (pendulum_indicator in desc) and (monster_indicator in desc):
        #desc: "[ Pendulum Effect ] \n<pendulum_effect> \n\n[ Monster Effect ] \n<monster_effect>" (we only want the stuff inside <>)
        split_description = desc.split(monster_indicator)
        # the pendulum part currently is "[ Pendulum Effect ] \n<pendulum_effect> \n\n" we want just the <pendulum_effect> part
        pendulum_part = split_description[0].replace(pendulum_indicator, "").strip()
        # the monster part currently is "\n<monster_effect>" we want just the <monster_effect> part
        monster_part = split_description[1].strip()

        return pendulum_part, monster_part
    return None, desc


#======================================== Api Calls ========================================#
def fetch_card_data(card_id:int|str):
    """Fetch card data from the YGOProDeck API."""
    try:
        response = requests.get(API_URL, params={"id": int(card_id)}, timeout=5)
        response.raise_for_status()
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            card_data = data["data"][0]
            return format_card(card_data)
        
    except requests.RequestException as e:
        print(f"Error fetching card data: {e}")
        return None

def fetch_all_cards_data() -> tuple[dict[str, list[dict]], list[dict]]:
    """Fetches all cards from the YGOProDeck API."""
    try:
        response = requests.get(API_URL, timeout=50)
        response.raise_for_status()
        data = response.json()
        monster_cards = []
        spell_cards = []
        trap_cards = []
        token_cards = []
        skill_cards = []
        other_cards = []
        sets:list[dict] = []

        if "data" in data:
            for card_data in data['data']:
                sets = update_sets(card_data.get('card_sets', []), sets)
                card_type, formatted_card = format_card(card_data)
                if card_type == "monster": monster_cards.append(formatted_card)
                elif card_type == "spell": spell_cards.append(formatted_card)
                elif card_type == "trap": trap_cards.append(formatted_card)
                elif card_type == "token": token_cards.append(formatted_card)
                elif card_type == "skill": skill_cards.append(formatted_card)
                else: other_cards.append(formatted_card)
        return {
            "monsters": monster_cards,
            "spells": spell_cards,
            "traps": trap_cards,
            "tokens": token_cards,
            "skills": skill_cards,
            "others": other_cards
        }, sets

    except requests.RequestException as e:
        print(f"Error fetching all cards data: {e}")
        return {}, []

# response = fetch_all_cards_data()
# with open("all_cards.json", "w", encoding="utf-8") as f:
#     json.dump(response, f, indent=4, ensure_ascii=False)
    