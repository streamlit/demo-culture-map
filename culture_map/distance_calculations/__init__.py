import enum
import typing

import pandas as pd
from scipy.spatial import distance
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

from culture_map.country_data import types

HOFSTEDE_DIMENSIONS = ['pdi', 'idv', 'mas', 'uai', 'lto', 'ind', 'ivr']
AVAILABLE_DISTANCES = {
    "Euclidean": distance.euclidean,
    "Cosine": distance.cosine,
    "Manhattan": distance.cityblock,
    "Correlation": distance.correlation

}
TO_PERCENT = 100.0
SQUARE = 2
PandasDataFrame = typing.TypeVar('pandas.core.frame.DataFrame')


class DimensionalityReductionAlgorithm(enum.Enum):
    PCA = 1
    TSNE = 2


def compute_dimensions(
        countries: types.Countries
) -> PandasDataFrame:
    index = [country.title for country in countries]
    dimensions = {}
    for dimension in HOFSTEDE_DIMENSIONS:
        row = []
        for country in countries:
            row.append(max(getattr(country, dimension) or 0, 0))
        dimensions[dimension] = row
    return pd.DataFrame(dimensions, index=index).transpose()


def compute_distance(
        country_from: types.CountryInfo,
        country_to: types.CountryInfo,
        distance_metric: str
) -> float:
    from_array = [max(getattr(country_from, dimension) or 0, 0) for dimension in HOFSTEDE_DIMENSIONS]
    to_array = [max(getattr(country_to, dimension) or 0, 0) for dimension in HOFSTEDE_DIMENSIONS]
    return AVAILABLE_DISTANCES[distance_metric](from_array, to_array)


@st.cache
def compute_distances(
        countries: types.Countries,
        distance_metric: str
) -> tuple[PandasDataFrame, float]:
    index = [country.title for country in countries]
    distances = {}
    max_distance = 0
    for country_from in countries:
        row = []
        for country_to in countries:
            distance = compute_distance(country_from, country_to, distance_metric)
            max_distance = max(max_distance, distance)
            row.append(distance)
        distances[country_from.title] = row
    return pd.DataFrame(distances, index=index), max_distance


@st.cache
def normalise_distance_matrix(
        distances: PandasDataFrame,
        max_distance: float
) -> PandasDataFrame:
    return distances.applymap(lambda x: x / max_distance * TO_PERCENT)


@st.cache
def generate_2d_coords(
        dimensions: PandasDataFrame,
        algorithm: DimensionalityReductionAlgorithm
) -> PandasDataFrame:
    reduced = None
    if algorithm == DimensionalityReductionAlgorithm.PCA:
        reduced = PCA(n_components=2)
    elif algorithm == DimensionalityReductionAlgorithm.TSNE:
        reduced = TSNE(n_components=2, perplexity=dimensions.shape[1] - 1, n_iter=300)
    return pd.DataFrame(reduced.fit_transform(dimensions.transpose()), index=dimensions.columns)

