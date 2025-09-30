import os
import time
import docker
import docker.errors
import json
import subprocess
import requests
from util.config import get_config, CARDS_INIT_PATH, COLLECTION_INIT_PATH
from util.db_connection import get_db_connection, DBConnection
from init.ygo_api import fetch_all_cards_data

try: #Load config or create a default one
    config = get_config()
    container_name:str = config.get("container_name", "yugioh_db")
    db_settings:dict = config.get("db", {})
    db_host:str = db_settings.get("host", "localhost")
    db_port:int = db_settings.get("port", 3306)
    db_name:str = db_settings.get("name", "ygo")
    db_user:str = db_settings.get("user", "user1")
    db_password:str = db_settings.get("password", "password")

except FileNotFoundError as e:
    print(e)
    input("Press Enter to exit...")
    exit(1)


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
    try: #remove existing container if it exists
        existing_container = client.containers.get(container_name)
        print(f"Removing existing container {container_name}...")
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
        name=container_name,
        environment={
            "MYSQL_ROOT_PASSWORD": db_password,
            "MYSQL_DATABASE": db_name,
            "MYSQL_USER": db_user,
            "MYSQL_PASSWORD": db_password,
        },
        ports={f"{db_port}/tcp": db_port},
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
        cmd=f"mysqladmin ping -h {db_host} -P {db_port} -u {db_user} -p{db_password}",
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


db:DBConnection = get_db_connection()

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

# print("Fetching card data from YGOProDeck API (this may take a while)...")
# all_cards, sets = fetch_all_cards_data()
# print(f"Fetched data for {sum(len(cards) for cards in all_cards.values())} cards across {len(sets)} sets.")

# print("adding sets to database...")
# for card_set in sets:
#     pass #TODO: insert sets into db
# print("Sets added to database.")


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