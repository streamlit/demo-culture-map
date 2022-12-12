import random

import streamlit as st

from culture_map import country_data

DEFAULT_COUNTRY_NUMBER = 4

all_countries_names = country_data.get_all_country_names()
if "default_countries" not in st.session_state:
    st.session_state["default_countries"] = random.choices(all_countries_names, k=DEFAULT_COUNTRY_NUMBER)

st.title("🌎 Culture map app")

st.header("The 6-D model of national culture 🗺️")

st.markdown(open('culture_map/scripts/intro.md').read())

selected_countries = st.multiselect(
    'Choose countries you want to compare',
    all_countries_names,
    st.session_state["default_countries"])

st.write('You selected:', selected_countries)