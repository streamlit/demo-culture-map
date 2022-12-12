import streamlit as st

from culture_map.country_data import download
from culture_map.country_data import serialise
from culture_map.country_data import types

COUNTRY_DATA: types.Countries = serialise.json_to_countries(download.download_country_data())


@st.cache
def get_country_dict() -> dict[str, types.CountryInfo]:
    return {country.title: country for country in COUNTRY_DATA}
