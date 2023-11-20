from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import string
import re
import time

''' Try to find pokemon name in pokedex '''
def try_find_in_pokedex(full_name : str):
    # Special conditions
    if "porygon 2" in full_name.lower():
        full_name = full_name.replace("Porygon 2", "Porygon2")

    if "nidoran" in full_name.lower():
        return ("(29f, 32m)","","")
    
    if "doll" in full_name.lower():
        return(None, "", "")

    # Try to get full name
    dex_num = pokedex.get(full_name.lower())

    if dex_num is None and " " in full_name and "&" not in full_name:

        name_split = full_name.split()

        # At first, try to just cut the last part and set it as suffix
        dex_num = pokedex.get(" ".join(name_split[:-1]).lower())
        if dex_num is not None:
            return (dex_num, "", name_split[-1])
        
        # Then try to cut the prefix only
        dex_num = pokedex.get(" ".join(name_split[1:]).lower())
        if dex_num is not None:
            return (dex_num, name_split[0], "")
        
        # Then both
        dex_num = pokedex.get(" ".join(name_split[1:-1]).lower())
        if dex_num is not None:
            return(dex_num, name_split[0], name_split[-1])
        
        # And now just try every individual combination
        for i in range(len(name_split)):
            for j in range(i, len(name_split)):
                dex_num = pokedex.get(" ".join(name_split[i:j]).lower())
                if dex_num is not None:
                    return (dex_num, " ".join(name_split[:i]), " ".join(name_split[j:]))

        # And one last chance, try to parse it with dash also
        name_split_dash = re.split("-| ", full_name)
        for i in range(len(name_split_dash)):
            dex_num = pokedex.get(" ".join(name_split_dash[i]).lower())
            if dex_num is not None:
                return (dex_num, " ".join(name_split_dash[:i]), " ".join(name_split_dash[i:]))

        return (None, "", "")
    else:
        return (dex_num, "", "")

''' Filter only printable chars '''
def to_print(s : str):
    return ''.join([x for x in s if x in string.printable])

''' Stopwatch (from borrowed from https://www.codespeedy.com/how-to-create-a-stopwatch-in-python/)'''
def time_lapsed(start, end):
  sec = end - start
  mins = sec // 60
  sec = sec % 60
  hours = mins // 60
  mins = mins % 60
  print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),sec))

''' Main '''
start_time = time.time()

pokedex = {}
pokedex_file = open("pokedex.csv", "r")
pokedex_file.readline()
pokedex_csv = pokedex_file.readlines()
pokedex_file.close()

for pokeline in pokedex_csv:
    pokeline_parsed = pokeline.split(",")
    pokedex[pokeline_parsed[1].lower()] = pokeline_parsed[0]

options = webdriver.ChromeOptions()

options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--headless')

driver = webdriver.Edge(options=options)
driver.get("https://www.pokellector.com/sets")

sets_element = driver.find_element(By.ID, "columnLeft")
set_names = sets_element.find_elements(By.CLASS_NAME, "set")
sets_listing = sets_element.find_elements(By.CLASS_NAME, "buttonlisting")

set_names_file = open("set_names.txt", "w")

index = 0
set_links = []
for i in range(len(set_names) - 1, -1, -1):
    name = set_names[i].accessible_name

    if "Topps" in name:
        continue

    listing = sets_listing[i]
    sets = listing.find_elements(By.CLASS_NAME, "button")
    for j in range(len(sets) -1, -1, -1):
        set = sets[j]
        title = set.get_attribute("title")[:-4]
        link = set.get_attribute("href")
        set_links.append(link)
        
        set_names_file.write(f'{index};{name};{title};{link}\n')

        index += 1

set_names_file.close()

master_file = open("master.txt", "w")
master_file.write("ID;Card title;Full card name;Prefix;Suffix;Card #;Pokémon;Set\n")
id = 0

# for index in range(1):
#     link = set_links[index]
    # driver.get("https://www.pokellector.com/English-XY-Promos-Expansion/")
    # driver.get("https://www.pokellector.com/Great-Encounters-Expansion/")
    # driver.get("https://www.pokellector.com/Scarlet-Violet-151-Expansion/")
    # driver.get("https://www.pokellector.com/Team-Up-Expansion/")
for index in range(len(set_links)):
    driver.get(set_links[index])
    card_listings = driver.find_element(By.CLASS_NAME, "cardlisting")
    cards = card_listings.find_elements(By.XPATH, "div[contains(@class,'card')]")

    for card in cards:
        card_title = card.find_element(By.TAG_NAME, "a").get_attribute("title")
        card_title_parsed = re.split("(\([^\)]*\))* - ", card_title)
        last_name_split = card_title_parsed[-1].split("#")
        
        if len(last_name_split) >= 2:
            num = last_name_split[-1]
        else:
            num = ""

        full_name = to_print(card_title_parsed[0].strip())

        (dex_num, prefix, suffix) = try_find_in_pokedex(full_name)

        if dex_num is None:
            dex_num = 0

        if suffix is None:
            suffix = ""

        if prefix is None:
            prefix = ""
        
        master_file.write(f'{id};{to_print(card_title)};{full_name};{prefix};{suffix};{num};{dex_num};{index}\n')
        id += 1

master_file.close()
driver.quit()

end_time = time.time()
time_lapsed(start_time, end_time)
