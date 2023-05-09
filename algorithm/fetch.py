from pathlib import Path
import requests 


def fetch_map_from_bounding_box(filename , top, bottom, left right):
    url = "https://overpass-api.de/api/map?bbox={left},{bottom},{right},{top}"
    filename = Path(filename)
    response = requests.get(url)
    filename.write_bytes(response.content)
    print(f"map : {filename} has been fetched successfully ")