from culture_map.country_data import types


def json_to_countries(raw_data: types.JSONType) -> types.Countries:
    return [serialise_country(country) for country in raw_data]


# TODO: use json schema to the likes
def serialise_country(raw_data: types.JSONType) -> types.CountryInfo:
    return types.CountryInfo(
        raw_data['id'],
        raw_data['title'],
        raw_data['slug'],
        int(raw_data['pdi']) if raw_data['pdi'] else None,
        int(raw_data['idv']) if raw_data['idv'] else None,
        int(raw_data['mas']) if raw_data['mas'] else None,
        int(raw_data['uai']) if raw_data['uai'] else None,
        int(raw_data['lto']) if raw_data['lto'] else None,
        int(raw_data['ind']) if raw_data['ind'] else None,
        int(raw_data['ivr']) if raw_data['ivr'] else None,
        raw_data['adjective']
    )