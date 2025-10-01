from flask import Blueprint
from util.ygo_api import fetch_all_cards_data
from modules import sets
from modules.cards import monsters, spells, traps, skills, tokens
import time

bp = Blueprint('base_api', __name__)

@bp.route('/init', methods=['POST'])
def initalize_data():
    """ Initialize the database with card data from the YGO API. """
    try:

        print("Fetching card data from YGOProDeck API (this may take a while)...")
        all_cards, all_sets = fetch_all_cards_data()

        monster_count = len(all_cards.get('monsters', []))
        spell_count = len(all_cards.get('spells', []))
        trap_count = len(all_cards.get('traps', []))
        token_count = len(all_cards.get('tokens', []))
        skill_count = len(all_cards.get('skills', []))
        total_count = monster_count + spell_count + trap_count + token_count + skill_count

        print(f"Fetched {total_count} cards over {len(all_sets)} sets from the API. (Monsters: {monster_count}, Spells: {spell_count}, Traps: {trap_count}, Tokens: {token_count}, Skills: {skill_count})")

        print("adding sets to database...")
        for set_data in all_sets:
            sets.add(
                set_code=set_data.get('set_code', ""),
                set_name=set_data.get('set_name', "")
            )
        print("Sets added.")

        print("adding monster cards to database...")
        for monster_card in all_cards.get('monsters', []):
            print (f"Attempting to add monster card: {monster_card.get('name', '')} (ID: {monster_card.get('id', 0)})")
            monsters.add(
                id=monster_card.get('id', 0),
                name=monster_card.get('name', ""),
                description=monster_card.get('description', ""),
                image_url=monster_card.get('image_url', ""),
                small_image_url=monster_card.get('image_url_small', ""),
                lookup_url=monster_card.get('api_url', ""),
                attribute=monster_card.get('attribute', ""),
                level=monster_card.get('level'),
                types=monster_card.get('types', []),
                attack=monster_card.get('atk', 0),
                defense=monster_card.get('def', 0),
                link_markers=monster_card.get('link_markers'),
                link_value=monster_card.get('link_value'),
                pendulum_scale=monster_card.get('pendulum_scale'),
                pendulum_effect=monster_card.get('pendulum_effect')
            )
            time.sleep(0.2) #to avoid hitting the rate limit of the api we slow down the requests so at most we do 10 requests per second or 5 cards per second
        print("Monster cards added.")

        print("adding spell cards to database...")
        for spell_card in all_cards.get('spells', []):
            print (f"Attempting to add spell card: {spell_card.get('name', '')} (ID: {spell_card.get('id', 0)})")
            spells.add(
                id=spell_card.get('id', 0),
                name=spell_card.get('name', ""),
                description=spell_card.get('description', ""),
                image_url=spell_card.get('image_url', ""),
                small_image_url=spell_card.get('image_url_small', ""),
                lookup_url=spell_card.get('api_url', ""),
                spell_type=spell_card.get('type', "")
            )
            time.sleep(0.2) #to avoid hitting the rate limit of the api we slow down the requests so at most we do 10 requests per second or 5 cards per second
        print("Spell cards added.")

        print("adding trap cards to database...")
        for trap_card in all_cards.get('traps', []):
            print (f"Attempting to add trap card: {trap_card.get('name', '')} (ID: {trap_card.get('id', 0)})")
            traps.add(
                id=trap_card.get('id', 0),
                name=trap_card.get('name', ""),
                description=trap_card.get('description', ""),
                image_url=trap_card.get('image_url', ""),
                small_image_url=trap_card.get('image_url_small', ""),
                lookup_url=trap_card.get('api_url', ""),
                trap_type=trap_card.get('type', "")
            )
            time.sleep(0.2) #to avoid hitting the rate limit of the api we slow down the requests so at most we do 10 requests per second or 5 cards per second
        print("Trap cards added.")

        print("adding token cards to database...")
        for token_card in all_cards.get('tokens', []):
            print (f"Attempting to add token card: {token_card.get('name', '')} (ID: {token_card.get('id', 0)})")
            tokens.add(
                id=token_card.get('id', 0),
                name=token_card.get('name', ""),
                description=token_card.get('description', ""),
                image_url=token_card.get('image_url', ""),
                small_image_url=token_card.get('image_url_small', ""),
                lookup_url=token_card.get('api_url', "")
            )
            time.sleep(0.2) #to avoid hitting the rate limit of the api we slow down the requests so at most we do 10 requests per second or 5 cards per second
        print("Token cards added.")

        print("adding skill cards to database...")
        for skill_card in all_cards.get('skills', []):
            print (f"Attempting to add skill card: {skill_card.get('name', '')} (ID: {skill_card.get('id', 0)})")
            skills.add(
                id=skill_card.get('id', 0),
                name=skill_card.get('name', ""),
                description=skill_card.get('description', ""),
                image_url=skill_card.get('image_url', ""),
                small_image_url=skill_card.get('image_url_small', ""),
                lookup_url=skill_card.get('api_url', "")
            )
            time.sleep(0.2) #to avoid hitting the rate limit of the api we slow down the requests so at most we do 10 requests per second or 5 cards per second
        print("Skill cards added.")

        return {"status": "success", "message": "Database initialized with card data."}, 200
    
    except Exception as e:
        print(f"Error during initialization: {e}")
        return {"status": "error", "message": str(e)}, 500
