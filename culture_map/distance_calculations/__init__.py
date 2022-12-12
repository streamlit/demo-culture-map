import typing

import pandas as pd

from culture_map.country_data import types

HOFSTEDE_DIMENSIONS = ['pdi', 'idv', 'mas', 'uai', 'lto', 'ind', 'ivr']
PandasDataFrame = typing.TypeVar('pandas.core.frame.DataFrame')


def compute_distance(country_from: types.CountryInfo, country_to: types.CountryInfo) -> float:
    return sum(
        [
            (int(getattr(country_from, dimension)) - int(getattr(country_to, dimension))) ** 2
            for dimension in HOFSTEDE_DIMENSIONS
        ]
    )


def compute_distances(countries: types.Countries) -> PandasDataFrame:
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
    return pd.DataFrame(distances, index=index)
