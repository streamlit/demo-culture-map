import streamlit as st

from culture_map.country_data import download
from culture_map.country_data import serialise
from culture_map.country_data import types

COUNTRY_DATA: types.Countries = serialise.json_to_countries(download.download_country_data())

@st.cache
def get_country_dict(
) -> dict[str, types.CountryInfo]:
    return {country.title: country for country in COUNTRY_DATA}


GROUPS_TO_COUNTRIES = {
    'MENA': [
        'Algeria',
        'Egypt',
        'Iran',
        'Iraq',
        'Israel',
        'Jordan',
        'Kuwait',
        'Lebanon',
        'Libya',
        'Morocco',
        'Qatar',
        'Saudi Arabia',
        'Syria',
        'Tunisia',
        'United Arab Emirates',
    ],
    'AFRICA': [
        'Ethiopia',
        'Kenya',
        'Tanzania',
        'São Tomé and Príncipe',
        'Angola',
        'Malawi',
        'Mozambique',
        'Namibia',
        'South Africa',
        'Zambia',
        'Burkina Faso',
        'Cape Verde',
        'Ghana',
        'Nigeria',
        'Senegal',
        'Sierra Leone'
    ],
    'EU': [
        'Austria',
        'Belgium',
        'Bulgaria',
        'Croatia',
        'Czech Republic',
        'Denmark',
        'Estonia',
        'Finland',
        'France',
        'Germany',
        'Greece',
        'Hungary',
        'Ireland',
        'Italy',
        'Latvia',
        'Lithuania',
        'Luxembourg',
        'Malta',
        'Netherlands',
        'Poland',
        'Portugal',
        'Romania',
        'Slovakia',
        'Slovenia',
        'Spain',
        'Sweden'
    ],
    'G20': [
        'Australia',
        'Canada',
        'Saudi Arabia',
        'United States',
        'India',
        'Russia',
        'South Africa',
        'Turkey',
        'Argentina',
        'Brazil',
        'Mexico',
        'France',
        'Germany',
        'Italy',
        'United Kingdom',
        'China',
        'Indonesia',
        'Japan',
        'South Korea'
    ],
    'LATAM': [
        'Argentina',
        'Bolivia',
        'Brazil',
        'Chile',
        'Colombia',
        'Costa Rica',
        'Dominican Republic',
        'Ecuador',
        'El Salvador',
        'Guatemala',
        'Honduras',
        'Mexico',
        'Panama',
        'Paraguay',
        'Peru',
        'Uruguay',
        'Venezuela'
    ],
    'AMERS': [
        'Canada',
        'United States',
        'Argentina',
        'Bolivia',
        'Brazil',
        'Chile',
        'Colombia',
        'Costa Rica',
        'Dominican Republic',
        'Ecuador',
        'El Salvador',
        'Guatemala',
        'Honduras',
        'Mexico',
        'Panama',
        'Paraguay',
        'Peru',
        'Uruguay',
        'Venezuela'
    ],
    'OPEC': [
        'Algeria',
        'Angola',
        'Iran',
        'Iraq',
        'Kuwait',
        'Libya',
        'Nigeria',
        'Saudi Arabia',
        'United Arab Emirates',
        'Venezuela'
    ]
}

COUNTRY_GROUPS = list(GROUPS_TO_COUNTRIES.keys())