import random

import streamlit as st

from culture_map import country_data
from culture_map import distance_calculations

DEFAULT_COUNTRY_NUMBER = 4

all_countries = country_data.get_country_dict()
all_countries_names = list(all_countries.keys())
if "default_countries" not in st.session_state:
    st.session_state["default_countries"] = random.choices(all_countries_names, k=DEFAULT_COUNTRY_NUMBER)

st.title("🌎 Culture map app")

st.header("The 6-D model of national culture 🗺️")

st.markdown(open('culture_map/scripts/intro.md').read())

selected_countries_names = st.multiselect(
    'Choose countries you want to compare',
    all_countries_names,
    st.session_state["default_countries"])

st.write('You selected:', selected_countries_names)

selected_countries = [country for country in all_countries.values() if country.title in selected_countries_names]

df = distance_calculations.compute_distances(selected_countries)
st.write(df)
