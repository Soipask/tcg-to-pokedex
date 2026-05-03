from modules.models import CardInfo

from pathlib import Path

allowed_special = set()
translations = {}

def load_special_chars(path):
    result = set()

    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                result.add(int(line))

    return result


def load_translations(path):
    result = {}

    with open(path, encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            left, right = line.split(";")

            left_chars = "".join(chr(int(x)) for x in left.split())
            right_chars = "".join(chr(int(x)) for x in right.split())

            result[left_chars] = right_chars

    return result


def initialize_special_chars():
    global allowed_special
    global translations

    # TODO: Maybe think about if we need allowed "special" (non-ASCII) chars if we translate them out 
    # (and if not in the combination specified in translations 
    # (like for "206 180 -> 948" we don't need to allow 206 alone and replace using translations already filters out the wrong chars)
    allowed_special = load_special_chars(
        Path("data/allowed_special_chars.txt")
    )

    translations = load_translations(
        Path("data/special_chars_translation.csv")
    )


def to_print(text: str):
    # Apply translations
    for old, new in translations.items():
        text = text.replace(old, new)

    result = []
    removed = []

    for char in text.strip():
        code = ord(char)

        if char.isprintable() or code in allowed_special:
            result.append(char)
        else:
            removed.append(f"{char} ({code} / {hex(code)})")

    if removed:
        print(f"Filtered from '{text}': {', '.join(removed)}")

    return "".join(result)

def parse_name(card : CardInfo):
    card.card_title = to_print(card.card_title)
    card_title = card.card_title.replace("&amp;", "&")
    card_title_parsed = card_title.split(" - ")
    # TODO: Smart parsing? for e.g. 7507;Gym Badge (Brock - Boulder) - XY Promos #203;Gym Badge (Brock;... (ignore " - " inside brackets?)
    last_name_split = card_title_parsed[-1].split("#")
    
    if len(last_name_split) >= 2:
        num = last_name_split[-1]
    else:
        num = ""

    full_name = to_print(card_title_parsed[0].strip())

    card.card_number = num
    card.full_name = full_name

'''for debugging purposes'''
def parse_card(card_data_param : str, parse_whole : bool):
    card_data = card_data_param.strip()
    card_split = card_data.split(";")
    if len(card_split) == 8:
        card = CardInfo(card_split[0], card_split[1], card_split[7])
        if (parse_whole):
            card.full_name = card_split[2]
            card.prefix = card_split[3]
            card.suffix = card_split[4]
            card.card_number = card_split[5]
            card.pokemon = card_split[6]
    else:
        return None
    
    return card

