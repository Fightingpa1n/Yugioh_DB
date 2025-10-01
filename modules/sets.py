from util.db_connection import get_db


#======================================== Sets ========================================#
def add(set_code:str, set_name:str):
    """ Add a card set to the database.
        - set_code(str): The unique code of the set (e.g., "LOB").
        - set_name(str): The name of the set (e.g., "Legend of Blue Eyes White Dragon").
    """
    try:
        get_db().execute(
            """
            INSERT IGNORE INTO `sets` (`name`, `code`)
            VALUES (%s, %s)
            """,
            (set_name, set_code)
        )
    except Exception as e:
        print(f"Error adding card set: {e}")
