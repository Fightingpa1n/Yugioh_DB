import os
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) #root directory
CONFIG_PATH = os.path.join(ROOT_DIR, "config.json") #config file path
CARDS_INIT_PATH = os.path.join(ROOT_DIR, "db", "cards_init.sql") #cards init file path
COLLECTION_INIT_PATH = os.path.join(ROOT_DIR, "db", "collection_init.sql") #collection init file path

default_config = {
    "container_name": "yugioh_db",
    "db": {
        "host": "localhost",
        "port": 3306,
        "name": "ygo",
        "user": "user1",
        "password": "password"
    }
}

def get_config():
    """load config from config.json or create a default one if it doesn't exist"""
    config = default_config.copy() #start with default config
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'w') as file:
            json.dump(default_config, file, indent=4)
        raise FileNotFoundError(f"Created default config file at {CONFIG_PATH}. Please edit it with your database settings.")
    else:
        with open(CONFIG_PATH, 'r') as file:
            config.update(json.load(file)) #update default config with values from file
    return config
