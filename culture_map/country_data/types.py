import dataclasses
import typing

JSONType = typing.Union[str, int, float, bool, None, typing.Mapping[str, 'JSON'], typing.List['JSON']]


@dataclasses.dataclass
class CountryInfo:
    id: int
    title: str
    slug: str
    pdi: int | None
    idv: int | None
    mas: int | None
    uai: int | None
    lto: int | None
    ind: int | None
    ivr: int | None
    adjective: str | None


Countries = list[CountryInfo]
