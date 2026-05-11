from modules.models import CardInfo

from dataclasses import dataclass

@dataclass
class Token:
    text: str
    normalized: str
    start: int
    end: int

@dataclass
class Match:
    pokemon: str
    dex: str
    start: int
    end: int

NIDORAN = "nidoran"

NORMALIZATION_REPLACEMENTS = {
    "é": "e",
    "'": "",
    ".": "",
    "-": " ",
    "&": " ",
    ",": " ",
}

# Characters that would after normalization potentially create new tokens
SEPARATORS = {
    " ",
    "\t",
    "\n",
    "-",
    ",",
    "&"
}

def normalize(text: str) -> str:
    ''' Normalizes name for better matching. Returns normalized string. '''
    text = text.lower()

    # replacing special chars
    for old, new in NORMALIZATION_REPLACEMENTS.items():
        text = text.replace(old, new)

    text = text.strip()

    return text

def apply_special_matching_conditions(name : str):
    ''' Applies some special conditions before matching. Returns new string to match.'''
    if "Porygon 2" in name:
        name = name.replace("Porygon 2", "Porygon2")
    
    return name

def tokenize(text: str) -> list[Token]:
    # and some special matching
    text = apply_special_matching_conditions(text)
    
    tokens = []

    token_start = None

    for i, char in enumerate(text):

        if char in SEPARATORS:

            if token_start is not None:
                token_text = text[token_start:i]

                tokens.append(Token(
                    text=token_text,
                    normalized=normalize(token_text),
                    start=token_start,
                    end=i
                ))

                token_start = None

        else:
            if token_start is None:
                token_start = i

    # Last token
    if token_start is not None:
        token_text = text[token_start:]

        tokens.append(Token(
            text=token_text,
            normalized=normalize(token_text),
            start=token_start,
            end=len(text)
        ))

    return tokens

class Matcher:

    def __init__(self):
        self.pokedex = {}
        pokedex_file = open("data/pokedex.csv", "r", encoding="utf-8")
        pokedex_file.readline()
        pokedex_csv = pokedex_file.readlines()
        pokedex_file.close()
        
        for pokeline in pokedex_csv:
            pokeline_parsed = pokeline.strip().split(",")
            self.pokedex[normalize(pokeline_parsed[1].lower())] = pokeline_parsed[0]

    def find_pokemon(self, text: str):
        normalized = normalize(text)
        return self.pokedex.get(normalized)

    def try_match_nidoran(self, card: CardInfo):
        full_name_lower = card.full_name.lower()

        if NIDORAN not in full_name_lower:
            return False

        nidoran_pos = full_name_lower.find(NIDORAN)

        # Everything before Nidoran
        card.prefix = card.full_name[:nidoran_pos].strip()

        after = card.full_name[nidoran_pos + len(NIDORAN):]

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
        # card.pokemon = "(29f/32m)"
        # There's only one ambiguous card on the site as of right now and that's male one
        card.pokemon = "32"
        card.suffix = after.strip()

        return True

    def try_match(self, card: CardInfo):
        if self.try_match_nidoran(card):
            return True
        
        tokens = tokenize(card.full_name)

        matches = []
        start = 0
        while start < len(tokens):

            found_match = False

            # Try longer combinations first
            for end in range(len(tokens), start, -1):
                candidate = " ".join(
                    token.normalized
                    for token in tokens[start:end]
                )
                dex_num = self.find_pokemon(candidate)

                if dex_num is not None:
                    matches.append(Match(
                        candidate, 
                        dex_num, 
                        tokens[start].start, 
                        tokens[end - 1].end)
                    )

                    start = end
                    found_match = True
                    break

            # Nothing matched at this position
            if not found_match:
                start += 1

        if len(matches) == 0:
            return False

        # Pokemon numbers
        card.pokemon = "/".join(match.dex for match in matches)

        # Prefix
        first_match = matches[0]
        card.prefix = card.full_name[:first_match.start].strip()

        # Suffix
        last_match = matches[-1]
        card.suffix = card.full_name[last_match.end:].strip()

        return True

    def match(self, card: CardInfo):
        if not self.try_match(card):
            card.pokemon = 0
            card.prefix = ""
            card.suffix = ""