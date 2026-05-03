from modules.models import CardInfo

class Matcher:

    def __init__(self):
        self.pokedex = {}
        pokedex_file = open("data/pokedex.csv", "r", encoding="utf-8")
        pokedex_file.readline()
        pokedex_csv = pokedex_file.readlines()
        pokedex_file.close()
        
        for pokeline in pokedex_csv:
            pokeline_parsed = pokeline.strip().split(",")
            self.pokedex[pokeline_parsed[1].lower()] = pokeline_parsed[0]

    def apply_special_matching_conditions(self, card : CardInfo):
        # Special conditions
        if "porygon 2" in card.full_name.lower():
            card.full_name = card.full_name.replace("Porygon 2", "Porygon2")
        # TODO: Match "Porygon 2"/"Flabebe" to "Porygon2"/"Flabébé" without changing card's full_name
        # e.g.: 7622;Flabebe - XY Flashfire #62

    def try_match_beginning(self, card : CardInfo, name_split : list[str]):
        # At first, try to just cut the last part and set it as suffix
        dex_num = self.pokedex.get(" ".join(name_split[:-1]).lower())
        if dex_num is not None:
            card.pokemon = dex_num
            card.prefix = ""
            card.suffix = name_split[-1]
            return
        card.pokemon = None
            
    def try_match_end(self, card : CardInfo, name_split : list[str]):
        dex_num = self.pokedex.get(" ".join(name_split[1:]).lower())
        if dex_num is not None:
            card.pokemon = dex_num
            card.prefix = name_split[0]
            card.suffix = ""
            return
        
    def try_match_every_combination(self, card : CardInfo, name_split : list[str]):
        dex_num = self.pokedex.get(" ".join(name_split[1:-1]).lower())
        if dex_num is not None:
            card.pokemon = dex_num
            card.prefix = name_split[0]
            card.suffix = name_split[-1]
            return
        
        # And now just try every individual combination
        for i in range(len(name_split)):
            for j in range(i + 1, len(name_split)):
                dex_num = self.pokedex.get(" ".join(name_split[i:j]).lower())
                if dex_num is not None:
                    card.pokemon = dex_num
                    card.prefix = " ".join(name_split[:i])
                    card.suffix = " ".join(name_split[j:])
                    return
                
        card.pokemon = 0
        card.prefix = ""
        card.suffix = ""

    def try_match_nidoran(self, card: CardInfo):
        full_name_lower = card.full_name.lower()

        if "nidoran" not in full_name_lower:
            return False

        nidoran_pos = full_name_lower.find("nidoran")

        # Everything before Nidoran
        card.prefix = card.full_name[:nidoran_pos].strip()

        after = card.full_name[nidoran_pos + len("nidoran"):]

        # Remove spaces/opening brackets before gender
        after = after.lstrip(" ([{")

        gender_char = None

        if len(after) > 0:
            gender_char = after[0]

        female_sign = chr(9792)  # ♀
        male_sign = chr(9794)    # ♂

        # Female
        if gender_char is not None:
            if gender_char.lower() == "f" or gender_char == female_sign:
                card.pokemon = self.pokedex.get("nidoranf")
                card.suffix = after[1:].lstrip(" )]}").strip()
                return True

            # Male
            if gender_char.lower() == "m" or gender_char == male_sign:
                card.pokemon = self.pokedex.get("nidoranm")
                card.suffix = after[1:].lstrip(" )]}").strip()
                return True

        # Unknown / ambiguous
        card.pokemon = "(29f/32m)"
        card.suffix = after.strip()

        return True

    def try_match(self, card : CardInfo):
        # Try to get full name
        card.pokemon = self.pokedex.get(card.full_name.lower())

        self.try_match_nidoran(card)

        if card.pokemon is None and " " in card.full_name and "&" not in card.full_name:
            name_split = card.full_name.split()

            # At first, try to just cut the last part and set it as suffix
            self.try_match_beginning(card, name_split)

            if card.pokemon is None or card.pokemon == 0:
                # Then try to cut the prefix only
                self.try_match_end(card, name_split)
            
            # Then both
            if card.pokemon is None or card.pokemon == 0:
                self.try_match_every_combination(card, name_split)
        else:
            if card.pokemon is None:
                card.pokemon = 0
            card.prefix = ""
            card.suffix = ""

    ''' Try to find pokemon name in pokedex '''
    def try_find(self, card : CardInfo):
        self.apply_special_matching_conditions(card)

        self.try_match(card)
