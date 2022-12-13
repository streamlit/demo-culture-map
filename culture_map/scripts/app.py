import random

import streamlit as st
import matplotlib.pyplot as plt

from culture_map import country_data
from culture_map import distance_calculations
from culture_map import visualisation

DEFAULT_COUNTRY_NUMBER = 10

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

distance_metric = st.selectbox('What distance metric would you like to use?',
                               list(distance_calculations.AVAILABLE_DISTANCES.keys()))

distances, max_distance = distance_calculations.compute_distances(selected_countries, distance_metric)
st.write('Country distances before normalisation:', distances)

normalised_distances = distance_calculations.normalise_distance_matrix(distances, max_distance)
st.write('Country distances after normalisation:', normalised_distances)

dimensions = distance_calculations.compute_dimensions(selected_countries)
st.write('Dimensions:', dimensions.transpose())
fig, ax = plt.subplots(figsize=(15, 15))
dimensions.plot.bar(ax=ax)
st.pyplot(fig)

show_clusters = st.checkbox('Show clusters', value=True)
heatmap = visualisation.generate_heatmap(normalised_distances, show_clusters)
st.pyplot(heatmap)
