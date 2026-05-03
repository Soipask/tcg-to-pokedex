from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

from modules.models import CardInfo, SetInfo

class CardScraper:
    TOPPS_NAME = "topps"

    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument('--headless')
        self.options.add_argument("--log-level=3")

        self.driver = webdriver.Chrome(options=self.options)
        
    def get_sets(self):
        self.driver.get("https://www.pokellector.com/sets")

        sets_element = self.driver.find_element(By.ID, "columnLeft")
        series_names = sets_element.find_elements(By.CLASS_NAME, "set")
        series_listing = sets_element.find_elements(By.CLASS_NAME, "buttonlisting")

        sets = []
        index = 0
        for i in range(len(series_names) - 1, -1, -1):
            series_name = series_names[i].accessible_name

            if self.TOPPS_NAME in series_name.lower():
                continue
                
            listing = series_listing[i]
            set_names = listing.find_elements(By.CLASS_NAME, "button")
            for j in range(len(set_names) -1, -1, -1):
                set_name = set_names[j]
                title = set_name.get_attribute("title")[:-4]
                url = set_name.get_attribute("href")
                
                set = SetInfo(index, series_name, title, url)
                sets.append(set)

                index += 1
        
        return sets
    
    def get_cards(self, sets: list[SetInfo]):
        id = 0
        cards = []
        for set in sets:
            self.driver.get(set.url)
            card_listings = self.driver.find_element(By.CLASS_NAME, "cardlisting")
            card_names = card_listings.find_elements(By.CSS_SELECTOR, "div.card")

            for card in card_names:
                card_title = card.find_element(By.TAG_NAME, "a").get_attribute("title")
                card = CardInfo(id=id, card_title=card_title, set_id=set.id)
                cards.append(card)
                id += 1
        
        return cards
    
    def dispose(self):
        self.driver.quit()