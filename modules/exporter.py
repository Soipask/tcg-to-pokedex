from pathlib import Path

from modules.models import SetInfo, CardInfo

def safe_open(path, mode="w", encoding="utf-8", max_attempts=100):
    path = Path(path)

    for i in range(max_attempts):
        if i == 0:
            candidate = path
        else:
            candidate = path.with_stem(f"{path.stem}_{i-1}")

        try:
            f = open(candidate, mode, encoding=encoding)
            print(f"Writing to: {candidate}")
            return f

        except PermissionError:
            continue

    raise RuntimeError("Could not open any output file")

def export_sets_write(sets : list[SetInfo]):
    with safe_open("data/exports/sets.txt") as set_names_file:
        for set in sets:
            set_names_file.write(f'{set.id};{set.series};{set.title};{set.url}\n')

def export_cards_write(cards : list[CardInfo]):
    with safe_open("data/exports/cards.txt") as master_file:
        master_file.write("ID;Card title;Full card name;Prefix;Suffix;Card #;Pokémon;Set\n")
        
        for card in cards:
            master_file.write(f'{card.id};{card.card_title};{card.full_name};{card.prefix};{card.suffix};{card.card_number};{card.pokemon};{card.set_id}\n')


def export_cards_write_debug(cards : list[CardInfo], path : str, mode : str):
    with safe_open(path, mode) as master_file:
        master_file.write("ID;Card title;Full card name;Prefix;Suffix;Card #;Pokémon;Set\n")
        
        for card in cards:
            master_file.write(f'{card.id};{card.card_title};{card.full_name};{card.prefix};{card.suffix};{card.card_number};{card.pokemon};{card.set_id}\n')
       