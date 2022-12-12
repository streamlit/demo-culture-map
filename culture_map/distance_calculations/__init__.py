import typing

import pandas as pd
import streamlit as st

from culture_map.country_data import types

HOFSTEDE_DIMENSIONS = ['pdi', 'idv', 'mas', 'uai', 'lto', 'ind', 'ivr']
TO_PERCENT = 100.0
SQUARE = 2
PandasDataFrame = typing.TypeVar('pandas.core.frame.DataFrame')


def compute_distance(country_from: types.CountryInfo, country_to: types.CountryInfo) -> float:
    return sum(
        [
            (int(getattr(country_from, dimension)) - int(getattr(country_to, dimension))) ** SQUARE
            for dimension in HOFSTEDE_DIMENSIONS
        ]
    )


@st.cache
def compute_distances(countries: types.Countries) -> tuple[PandasDataFrame, float]:
    index = [country.title for country in countries]
    distances = {}
    max_distance = 0
    for country_from in countries:
        row = []
        for country_to in countries:
            distance = compute_distance(country_from, country_to)
            max_distance = max(max_distance, distance)
            row.append(distance)
        distances[country_from.title] = row
    return pd.DataFrame(distances, index=index), max_distance


@st.cache
def normalise_distance_matrix(distances: PandasDataFrame, max_distance: float) -> PandasDataFrame:
    return distances.applymap(lambda x: x / max_distance * TO_PERCENT)

