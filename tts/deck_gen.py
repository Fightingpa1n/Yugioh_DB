import os
import json
from PIL import Image

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.db_connection import get_db_connection, DBConnection


CARD_WIDTH = 813
CARD_HEIGHT = 1185
CARD_AMOUNT = 70
PER_ROW = 10
PER_COL = 7

monster_path = "../assets/card_images/monsters"
spell_path = "../assets/card_images/spells"
trap_path = "../assets/card_images/traps"
token_path = "../assets/card_images/tokens"
skill_path = "../assets/card_images/skills"

all_decks = []

current_deck_id = 0
current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
current_deck_data = []

current_x = 0
current_y = 0
current_count = 0

db:DBConnection = get_db_connection()

for filename in os.listdir(monster_path): #loop through all files in the directory

    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(monster_path, filename)
        try:
            card_id = os.path.splitext(filename)[0]
            img = Image.open(img_path)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT))
            current_deck_img.paste(img, (current_x * CARD_WIDTH, current_y * CARD_HEIGHT))

            response = db.query("SELECT * FROM cards WHERE id = %s", (card_id,))
            card_data = response[0] if response else None

            if card_data:

                name = card_data["name"] #type: ignore
                if card_data["pendulum_effect"] is not None: #type: ignore
                    description = f"[Pendulum Effect]\n{card_data['pendulum_effect']}\n\n[Monster Effect]\n{card_data['description']}" #type: ignore
                else:
                    description = card_data["description"] #type: ignore

                current_deck_data.append({
                    "name": name,
                    "description": description
                })


            current_x += 1
            current_count += 1
            if current_x >= PER_ROW:
                current_x = 0
                current_y += 1
            
            if current_count >= CARD_AMOUNT: #save the current deck image
                deck_filename = f"monster_{current_deck_id}"
                current_deck_img.save(f"decks/monster/{deck_filename}.jpg")
                with open(f"decks/monster/{deck_filename}.json", 'w', encoding='utf-8') as file:
                    json.dump({
                        "cards": current_deck_data,
                        "amount": len(current_deck_data)
                    }, file, ensure_ascii=False, indent=4)
                
                print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
                all_decks.append({"filename": deck_filename})

                #reset for next deck
                current_deck_id += 1
                current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
                current_deck_data = []
                current_x = 0
                current_y = 0
                current_count = 0

        except Exception as e:
            print(f"Error processing {img_path}: {e}")


deck_filename = f"monster_{current_deck_id}"
current_deck_img.save(f"decks/monster/{deck_filename}.jpg")
with open(f"decks/monster/{deck_filename}.json", 'w', encoding='utf-8') as file:
    json.dump({
        "cards": current_deck_data,
        "amount": len(current_deck_data)
    }, file, ensure_ascii=False, indent=4)

print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
all_decks.append({"filename": deck_filename})

#reset for next deck
current_deck_id = 0
current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
current_deck_data = []
current_x = 0
current_y = 0
current_count = 0


for filename in os.listdir(spell_path): #loop through all files in the directory

    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(spell_path, filename)
        try:
            card_id = os.path.splitext(filename)[0]
            img = Image.open(img_path)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT))
            current_deck_img.paste(img, (current_x * CARD_WIDTH, current_y * CARD_HEIGHT))

            response = db.query("SELECT * FROM cards WHERE id = %s", (card_id,))
            card_data = response[0] if response else None

            if card_data:

                name = card_data["name"] #type: ignore
                description = card_data["description"] #type: ignore

                current_deck_data.append({
                    "name": name,
                    "description": description
                })


            current_x += 1
            current_count += 1
            if current_x >= PER_ROW:
                current_x = 0
                current_y += 1
            
            if current_count >= CARD_AMOUNT: #save the current deck image
                deck_filename = f"spell_{current_deck_id}"
                current_deck_img.save(f"decks/spell/{deck_filename}.jpg")
                with open(f"decks/spell/{deck_filename}.json", 'w', encoding='utf-8') as file:
                    json.dump({
                        "cards": current_deck_data,
                        "amount": len(current_deck_data)
                    }, file, ensure_ascii=False, indent=4)
                
                print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
                all_decks.append({"filename": deck_filename})

                #reset for next deck
                current_deck_id += 1
                current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
                current_deck_data = []
                current_x = 0
                current_y = 0
                current_count = 0

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

deck_filename = f"spell_{current_deck_id}"
current_deck_img.save(f"decks/spell/{deck_filename}.jpg")
with open(f"decks/spell/{deck_filename}.json", 'w', encoding='utf-8') as file:
    json.dump({
        "cards": current_deck_data,
        "amount": len(current_deck_data)
    }, file, ensure_ascii=False, indent=4)
print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
all_decks.append({"filename": deck_filename})

#reset for next deck
current_deck_id = 0
current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
current_deck_data = []
current_x = 0
current_y = 0
current_count = 0


for filename in os.listdir(trap_path): #loop through all files in the directory
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(trap_path, filename)
        try:
            card_id = os.path.splitext(filename)[0]
            img = Image.open(img_path)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT))
            current_deck_img.paste(img, (current_x * CARD_WIDTH, current_y * CARD_HEIGHT))

            response = db.query("SELECT * FROM cards WHERE id = %s", (card_id,))
            card_data = response[0] if response else None

            if card_data:

                name = card_data["name"] #type: ignore
                description = card_data["description"] #type: ignore

                current_deck_data.append({
                    "name": name,
                    "description": description
                })


            current_x += 1
            current_count += 1
            if current_x >= PER_ROW:
                current_x = 0
                current_y += 1
            
            if current_count >= CARD_AMOUNT: #save the current deck image
                deck_filename = f"trap_{current_deck_id}"
                current_deck_img.save(f"decks/trap/{deck_filename}.jpg")
                with open(f"decks/trap/{deck_filename}.json", 'w', encoding='utf-8') as file:
                    json.dump({
                        "cards": current_deck_data,
                        "amount": len(current_deck_data)
                    }, file, ensure_ascii=False, indent=4)
                
                print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
                all_decks.append({"filename": deck_filename})

                #reset for next deck
                current_deck_id += 1
                current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
                current_deck_data = []
                current_x = 0
                current_y = 0
                current_count = 0

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

deck_filename = f"trap_{current_deck_id}"
current_deck_img.save(f"decks/trap/{deck_filename}.jpg")
with open(f"decks/trap/{deck_filename}.json", 'w', encoding='utf-8') as file:
    json.dump({
        "cards": current_deck_data,
        "amount": len(current_deck_data)
    }, file, ensure_ascii=False, indent=4)
print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
all_decks.append({"filename": deck_filename})

#reset for next deck
current_deck_id = 0
current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
current_deck_data = []
current_x = 0
current_y = 0
current_count = 0

for filename in os.listdir(token_path): #loop through all files in the directory
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(token_path, filename)
        try:
            card_id = os.path.splitext(filename)[0]
            img = Image.open(img_path)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT))
            current_deck_img.paste(img, (current_x * CARD_WIDTH, current_y * CARD_HEIGHT))

            response = db.query("SELECT * FROM cards WHERE id = %s", (card_id,))
            card_data = response[0] if response else None

            if card_data:

                name = card_data["name"] #type: ignore
                description = card_data["description"] #type: ignore

                current_deck_data.append({
                    "name": name,
                    "description": description
                })


            current_x += 1
            current_count += 1
            if current_x >= PER_ROW:
                current_x = 0
                current_y += 1
            
            if current_count >= CARD_AMOUNT: #save the current deck image
                deck_filename = f"token_{current_deck_id}"
                current_deck_img.save(f"decks/token/{deck_filename}.jpg")
                with open(f"decks/token/{deck_filename}.json", 'w', encoding='utf-8') as file:
                    json.dump({
                        "cards": current_deck_data,
                        "amount": len(current_deck_data)
                    }, file, ensure_ascii=False, indent=4)
                
                print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
                all_decks.append({"filename": deck_filename})

                #reset for next deck
                current_deck_id += 1
                current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
                current_deck_data = []
                current_x = 0
                current_y = 0
                current_count = 0

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

deck_filename = f"token_{current_deck_id}"
current_deck_img.save(f"decks/token/{deck_filename}.jpg")
with open(f"decks/token/{deck_filename}.json", 'w', encoding='utf-8') as file:
    json.dump({
        "cards": current_deck_data,
        "amount": len(current_deck_data)
    }, file, ensure_ascii=False, indent=4)
print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
all_decks.append({"filename": deck_filename})

#reset for next deck
current_deck_id = 0
current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
current_deck_data = []
current_x = 0
current_y = 0
current_count = 0

for filename in os.listdir(skill_path): #loop through all files in the directory
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(skill_path, filename)
        try:
            card_id = os.path.splitext(filename)[0]
            img = Image.open(img_path)
            img = img.resize((CARD_WIDTH, CARD_HEIGHT))
            current_deck_img.paste(img, (current_x * CARD_WIDTH, current_y * CARD_HEIGHT))

            response = db.query("SELECT * FROM cards WHERE id = %s", (card_id,))
            card_data = response[0] if response else None

            if card_data:

                name = card_data["name"] #type: ignore
                description = card_data["description"] #type: ignore

                current_deck_data.append({
                    "name": name,
                    "description": description
                })


            current_x += 1
            current_count += 1
            if current_x >= PER_ROW:
                current_x = 0
                current_y += 1
            
            if current_count >= CARD_AMOUNT: #save the current deck image
                deck_filename = f"skill_{current_deck_id}"
                current_deck_img.save(f"decks/skill/{deck_filename}.jpg")
                with open(f"decks/skill/{deck_filename}.json", 'w', encoding='utf-8') as file:
                    json.dump({
                        "cards": current_deck_data,
                        "amount": len(current_deck_data)
                    }, file, ensure_ascii=False, indent=4)
                
                print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
                all_decks.append({"filename": deck_filename})

                #reset for next deck
                current_deck_id += 1
                current_deck_img = Image.new('RGB', (CARD_WIDTH * PER_ROW, CARD_HEIGHT * PER_COL), (255, 255, 255))
                current_deck_data = []
                current_x = 0
                current_y = 0
                current_count = 0

        except Exception as e:
            print(f"Error processing {img_path}: {e}")

deck_filename = f"skill_{current_deck_id}"
current_deck_img.save(f"decks/skill/{deck_filename}.jpg")
with open(f"decks/skill/{deck_filename}.json", 'w', encoding='utf-8') as file:
    json.dump({
        "cards": current_deck_data,
        "amount": len(current_deck_data)
    }, file, ensure_ascii=False, indent=4)
print(f"Saved {deck_filename}.jpg with {len(current_deck_data)} cards.")
all_decks.append({"filename": deck_filename})
db.close()

with open("decks/all_decks.json", 'w', encoding='utf-8') as file:
    json.dump({
        "decks": all_decks,
        "total_decks": len(all_decks)
    }, file, ensure_ascii=False, indent=4) 

input("Deck generation complete. Press Enter to exit...")

