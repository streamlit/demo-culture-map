import streamlit as st

from culture_map import country_data
from culture_map import distance_calculations
from culture_map import visualisation
from culture_map.country_data import types

st.title("Culture match")

st.header("Find your top matching countries")

PDI_HELP = "Power distance index (PDI): The power distance index is defined as " \
           "\"the extent to which the less powerful members of organizations and institutions (like the family) " \
           "accept and expect that power is distributed unequally\". " \
           "In this dimension, inequality and power is perceived from the followers, or the lower strata. " \
           "A higher degree of the Index indicates that hierarchy is clearly established and executed in society, " \
           "without doubt or reason. A lower degree of the Index signifies that people question authority and " \
           "attempt to distribute power."

IDV_HELP = "Individualism vs. collectivism (IDV): This index explores the \"degree to which people in a society are " \
           "integrated into groups\". Individualistic societies have loose ties that often only relate an " \
           "individual to his/her immediate family. They emphasize the \"I\" versus the \"we\". Its counterpart, " \
           "collectivism, describes a society in which tightly-integrated relationships tie extended families " \
           "and others into in-groups. These in-groups are laced with undoubted loyalty and support each other " \
           "when a conflict arises with another in-group."

MAS_HELP = "Masculinity vs. femininity (MAS): In this dimension, masculinity is defined as \"a preference in " \
           "society for achievement, heroism, assertiveness and material rewards for success\". Its counterpart " \
           "represents \"a preference for cooperation, modesty, caring for the weak and quality of life\". " \
           "Women in the respective societies tend to display different values. In feminine societies, they share " \
           "modest and caring views equally with men. In more masculine societies, women are somewhat assertive " \
           "and competitive, but notably less than men. In other words, they still recognize a gap between male " \
           "and female values. This dimension is frequently viewed as taboo in highly masculine societies."

UAI_HELP = "Uncertainty avoidance (UAI): The uncertainty avoidance index is defined as \"a society's tolerance " \
           "for ambiguity\", in which people embrace or avert an event of something unexpected, unknown, or " \
           "away from the status quo. Societies that score a high degree in this index opt for stiff codes of " \
           "behavior, guidelines, laws, and generally rely on absolute truth, or the belief that one lone truth " \
           "dictates everything and people know what it is. A lower degree in this index shows more acceptance of " \
           "differing thoughts or ideas. Society tends to impose fewer regulations, ambiguity is more accustomed " \
           "to, and the environment is more free-flowing."

LTO_HELP = "Long vs. short-term orientation (LTO): This dimension associates the connection of the past with the " \
           "current and future actions/challenges. A lower degree of this index (short-term) indicates that " \
           "traditions are honored and kept, while steadfastness is valued. Societies with a high degree in this " \
           "index (long-term) view adaptation and circumstantial, pragmatic problem-solving as a necessity. " \
           "A poor country that is short-term oriented usually has little to no economic development, while " \
           "long-term oriented countries continue to develop to a level of prosperity."

IND_HELP = "Indulgence vs. restraint (IND): This dimension refers to the degree of freedom that societal norms give " \
           "to citizens in fulfilling their human desires. Indulgence is defined as \"a society that allows " \
           "relatively free gratification of basic and natural human desires related to enjoying life and having " \
           "fun\". Its counterpart is defined as \"a society that controls gratification of needs and regulates it " \
           "by means of strict social norms\"."

st.text("1. Power distance")
pdi = st.slider('To which extent you accept that individuals in societies are not equal?', 0, 100, 50, help=PDI_HELP)

st.text("2. Individualism")
idv = st.slider('How independent you would like to be in your society?', 0, 100, 50, help=IDV_HELP)

st.text("3. Masculinity")
mas = st.slider('How much are you driven by competition, achievement and success and able to sacrifice caring for '
                'others and quality of life?', 0, 100, 50, help=MAS_HELP)

st.text("4. Uncertainty avoidance")
uai = st.slider('To which extent you feel threatened by ambiguous or unknown situations and try to avoid them ?',
                0, 100, 50, help=UAI_HELP)

st.text("5. Long term orientation")
lto = st.slider('How much do you consider past when dealing with future and present challenges?',
                0, 100, 50, help=LTO_HELP)

st.text("6. Indulgence")
ind = st.slider('To which extent you would like to express your desires and impulses??', 0, 100, 50, help=IND_HELP)

query = types.CountryInfo(500, "distance", "distance", pdi, idv, mas, uai, lto, ind, ind, None)

countries_dict = country_data.get_country_dict()
all_countries = list(countries_dict.values()) + [query]
distance_metric = st.selectbox('What distance metric would you like to use?',
                               list(distance_calculations.AVAILABLE_DISTANCES.keys()))
k = st.number_input('How many top countries to display?', value=4, min_value=1, max_value=len(all_countries)-1)

distances, max_distance = distance_calculations.compute_distances(all_countries, distance_metric)
normalised_distances = distance_calculations.normalise_distance_matrix(distances, max_distance)
ranking = normalised_distances.iloc[:, -1].sort_values()
st.write(ranking.iloc[1:k+1])
top_k = list(ranking.iloc[1:k+1].index)

top_k_countries = [countries_dict[country_name] for country_name in top_k]

dimensions = distance_calculations.compute_dimensions(top_k_countries)

radar = visualisation.generate_radar_plot(dimensions)
st.pyplot(radar)
