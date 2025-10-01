from util.db_connection import get_db
from util.data_handling import download_image
from modules.cards.types import get_card_type_id_by_name


#======================================== Skills ========================================#
def add(id:int, name:str, description:str, image_url:str, small_image_url :str, lookup_url:str):
    """ Add a skill card to the database.
        - id(int): The unique ID of the card.
        - name(str): The name of the card.
        - description(str): The card's description or effect text.
        - image_url(str): URL to the card's main image.
        - small_image_url(str): URL to the card's small image.
        - lookup_url(str): URL to the card's page on YGOProDeck.
    """
    try:
        image_name = f"{id}.jpg"
        image_path = f"assets/card_images/skills/{image_name}"
        small_image_path = f"assets/small_card_images/skills/{image_name}"

        download_image(image_url, image_path)
        download_image(small_image_url, small_image_path)

        get_db().execute(
            """
            INSERT IGNORE INTO `cards` (
                `id`, `type_id`, `name`, `description`,
                `image`, `small_image`, `lookup_url`
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                id,
                get_card_type_id_by_name("Skill"),
                name, description,
                image_path, small_image_path, lookup_url
            )
        )
    except Exception as e:
        print(f"Error adding skill card: {e}")
