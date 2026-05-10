import time
import os

from modules.matcher import Matcher
from modules.scraper import CardScraper
from modules.utils import time_lapsed
from modules.parser import parse_name, initialize_special_chars
from modules.exporter import export_sets_write, export_cards_write, export_cards_write_debug

start_time = time.time()
print(f"{time.localtime().tm_hour:02d}:{time.localtime().tm_min:02d}:{time.localtime().tm_sec:02d}")

if os.getenv("DEBUG"):
    debug_mode = True
else:
    debug_mode = False

print("Started scraping...")

scraper = CardScraper()
sets = scraper.get_sets()

initialize_special_chars()

if debug_mode:
    cards = scraper.get_cards(sets[2:3])
else:
    cards = scraper.get_cards(sets)

print("Finished scraping")
print("Starting matching...")

scraper.dispose()

matcher = Matcher()

for card in cards:
    parse_name(card)
    matcher.match(card)

print("Finished matching")
print("Started exporting...")

if debug_mode:
    export_cards_write_debug(cards, "data/exports/cards_debug.txt" ,"w")
else:
    export_sets_write(sets)
    export_cards_write(cards)

end_time = time.time()
print(f"Finished in: ")
time_lapsed(start_time, end_time)