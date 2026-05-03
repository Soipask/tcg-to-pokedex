import time

from modules.matcher import Matcher
from modules.scraper import CardScraper
from modules.utils import time_lapsed
from modules.parser import parse_name, initialize_special_chars
from modules.exporter import export_sets_write, export_cards_write, export_cards_write_debug

start_time = time.time()
print(f"{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}")
print("Started scraping...")

scraper = CardScraper()
sets = scraper.get_sets()

initialize_special_chars()

# cards = scraper.get_cards(sets[108:109])
cards = scraper.get_cards(sets)

print("Finished scraping\nStarting matching...")

scraper.dispose()

matcher = Matcher()

for card in cards:
    parse_name(card)
    matcher.try_find(card)

print("Finished matching\nStarted exporting...")

export_sets_write(sets)
export_cards_write(cards)
# export_cards_write_debug(cards, "data/exports/cards_debug.txt" ,"w")

end_time = time.time()
print(f"Finished in: ")
time_lapsed(start_time, end_time)