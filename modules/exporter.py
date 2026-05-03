from modules.models import SetInfo, CardInfo

def export_sets_write(sets : list[SetInfo]):
    set_names_file = open("data/exports/sets.txt", "w", encoding="utf-8")
    
    for set in sets:
        set_names_file.write(f'{set.id};{set.series};{set.title};{set.url}\n')
    
    set_names_file.close()

def export_cards_write(cards : list[CardInfo]):
    master_file = open("data/exports/cards.txt", "w", encoding="utf-8")
    master_file.write("ID;Card title;Full card name;Prefix;Suffix;Card #;Pokémon;Set\n")
    
    for card in cards:
        master_file.write(f'{card.id};{card.card_title};{card.full_name};{card.prefix};{card.suffix};{card.card_number};{card.pokemon};{card.set_id}\n')
    
    master_file.close()


def export_cards_write_debug(cards : list[CardInfo], path : str, mode : str):
    master_file = open(path, mode, encoding="utf-8")
    master_file.write("ID;Card title;Full card name;Prefix;Suffix;Card #;Pokémon;Set\n")
    
    for card in cards:
        master_file.write(f'{card.id};{card.card_title};{card.full_name};{card.prefix};{card.suffix};{card.card_number};{card.pokemon};{card.set_id}\n')
    
    master_file.close()
       