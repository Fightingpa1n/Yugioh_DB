import os
import requests

#======================================== Image Helper ========================================#
#==================== Image Download ====================#
def download_image(url:str, path:str):
    """Download an image from a URL to a local path."""
    try:
        if os.path.exists(path): return #if the file already exists
        os.makedirs(os.path.dirname(path), exist_ok=True) #create directory if it doesn't exist
        img_data = requests.get(url, timeout=10).content
        with open(path, 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

#======================================== Type Conversion Helpers ========================================#
#==================== Boolean/Integer ====================#
def boolean_to_int(value:bool|None) -> int|None:
    """Convert a boolean value to an integer (1 for True, 0 for False, None for None)."""
    if value is None:
        return None
    return 1 if value else 0

def int_to_boolean(value:int|None) -> bool|None:
    """Convert an integer value to a boolean (True for 1, False for 0, None for None)."""
    if value is None:
        return None
    return value == 1