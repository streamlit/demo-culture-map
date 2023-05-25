import json
from culture_map.country_data import types


def load_country_data(
) -> types.JSONType:
    with open("./culture_map/country_data/country.json", "r") as f:
        return json.load(f)
