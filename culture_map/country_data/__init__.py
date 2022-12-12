from culture_map.country_data import download
from culture_map.country_data import serialise
from culture_map.country_data import types

COUNTRY_DATA: types.Countries = serialise.json_to_countries(download.download_country_data())


def get_all_country_names() -> list[str]:
    return [country.title for country in COUNTRY_DATA]
