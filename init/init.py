import os
import time
import docker
import docker.errors
import json
import subprocess
import requests


ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(ROOT_DIR, "test_config.json")
CARDS_INIT_PATH = os.path.join(ROOT_DIR, "db", "cards_init.sql")
COLLECTION_INIT_PATH = os.path.join(ROOT_DIR, "db", "collection_init.sql")

import sys
sys.path.insert(0, ROOT_DIR)  #allow imports from root

from webapp.util.db_connection import DBConnection
from webapp.util.ygo_api import fetch_all_cards_data


default_config = {
    "container_name": "yugioh_db",
    "db": {
        "host":  "localhost",
        "port":  3306,
        "name":  "ygo",
        "user":  "Unnamed",
        "password":  "<ChangeMePls>"
    }
}

config = {}

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(default_config, f, indent=4)
    print(f"Created default config file at {CONFIG_PATH}. Please edit it with your database settings.")
    input("Press Enter to exit...")
    exit(0)
else:
    with open(CONFIG_PATH, 'r') as f:
        default_config.update(json.load(f))
        config = default_config
    print(f"Loaded config from {CONFIG_PATH}")

def is_docker_running():
    try:
        subprocess.check_output(["docker", "info"], stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

if not is_docker_running():
    print("Docker does not appear to be running. Please start Docker Desktop or your Docker service.")
    input("Press Enter to exit...")
    exit(1)

client = docker.from_env()
try:

    #remove existing container if it exists
    try:
        existing_container = client.containers.get(config["container_name"])
        print(f"Removing existing container {config['container_name']}...")
        existing_container.stop()
        existing_container.remove()
        print("Existing container removed.")
    except docker.errors.NotFound:
        pass
    
    # Pull the image if not present
    client.images.pull("mysql:8.0")

    # Run the container
    container = client.containers.run(
        "mysql:8.0",
        name=config["container_name"],
        environment={
            "MYSQL_ROOT_PASSWORD": config["db"]["password"],
            "MYSQL_DATABASE": config["db"]["name"],
            "MYSQL_USER": config["db"]["user"],
            "MYSQL_PASSWORD": config["db"]["password"]
        },
        ports={f"{config['db']['port']}/tcp": config['db']['port']},
        detach=True,
    )
    print(f"Container {container.name} started with ID {container.id}")


except Exception as e:
    print(f"Error starting container: {e}")
    print("Make sure Docker is running and no other container is using the same name or port.")
    input("Press Enter to exit...")
    exit(1)


#wait until the db is ready to accept connections

print("Waiting for database to be ready...", end="", flush=True)
time.sleep(5)  # Initial wait before checking
max_retries = 10
for i in range(max_retries):
    exit_code, output = container.exec_run(
        cmd=f"mysqladmin ping -h {config['db']['host']} -P {config['db']['port']} -u {config['db']['user']} -p{config['db']['password']}",
        demux=True
    )
    if exit_code == 0 and b'mysqld is alive' in output[0]:
        print("\nDatabase is ready!")
        break
    else:
        print(".", end="", flush=True)
        time.sleep(5)
else:
    print("\nDatabase did not become ready in time. Please check the container logs for more information.")
    input("Press Enter to exit...")
    exit(1)

#fill database with inital stuff
db:DBConnection = DBConnection(
    db_host=config["db"]["host"],
    db_port=config["db"]["port"],
    db_name=config["db"]["name"],
    db_user=config["db"]["user"],
    db_password=config["db"]["password"]
)

print("Initializing main tables...")
with open(CARDS_INIT_PATH, 'r', encoding='utf-8') as f:
    cards_sql = f.read()
    db.execute_script(cards_sql)
print("Main tables initialized.")

print("Initializing collection tables...")
with open(COLLECTION_INIT_PATH, 'r', encoding='utf-8') as f:
    collection_sql = f.read()
    db.execute_script(collection_sql)
print("Collection tables initialized.")

print("Fetching card data from YGOProDeck API (this may take a while)...")
all_cards, sets = fetch_all_cards_data()
print(f"Fetched data for {sum(len(cards) for cards in all_cards.values())} cards across {len(sets)} sets.")

print("adding sets to database...")
for card_set in sets:
    pass #TODO: insert sets into db
print("Sets added to database.")


# print("Adding cards to database (this may take a while)...")
# for card_type, cards in all_cards.items():
#     print(f"Adding {len(cards)} {card_type} cards...")

#     #add folder for each card type
#     image_folder = os.path.join(ROOT_DIR, "db", "card_images", card_type)
#     os.makedirs(image_folder, exist_ok=True)

#     for card in cards:
#         image_path = os.path.join(image_folder, f"{card['id']}.jpg")
#         card_id = db.execute("""
#             INSERT INTO cards () VALUES
#                 (
#                 );
#         """, [])
#         #download image
#         if 'image_url_small' in card and card['image_url_small']:
#             try:
#                 img_data = requests.get(card['image_url_small'], timeout=10).content
#                 with open(image_path, 'wb') as img_file:
#                     img_file.write(img_data)
#             except Exception as e:
#                 print(f"Failed to download image for card ID {card['id']}: {e}")
#         time.sleep(0.1) #slight delay to avoid hammering the API
# print("Cards added to database.")

db.close()

print("Initialization complete. You can now run the app using run.bat")