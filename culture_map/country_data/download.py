import requests
from culture_map.country_data import types

HOFSTEDE_COUNTRY_URL = "https://www.hofstede-insights.com/fi/wp-json/v1/country"


def download_country_data(
) -> types.JSONType:
    response = requests.get(HOFSTEDE_COUNTRY_URL)
    if not response.ok:
        return response.text
    return response.json()
