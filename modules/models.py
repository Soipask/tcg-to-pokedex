from dataclasses import dataclass, field

@dataclass
class SetInfo:
    id: int
    series: str
    title: str
    url: str

@dataclass
class CardInfo:
    id: int
    card_title: str
    full_name: str = field(init=False)
    prefix: str = field(init=False)
    suffix: str = field(init=False)
    card_number: str = field(init=False)
    pokemon: str = field(init=False)
    set_id: int