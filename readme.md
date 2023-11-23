## TCG to Pokedex linker

### Do you want to create real-time pokedex made from TCG cards?
You can check: https://docs.google.com/spreadsheets/d/1z1_Ck79Hp1Dl6eZRdi2RnorAQhA4IIDbDZkJhuU7Vw0/edit

You can check lookup tables on Sheets named *Pokemon lookup* and *Set lookup*. On these sheets, there's a dropdown menu that you should have access to, choosing a pokemon (or a set) will list you all cards with their basic information.

If you want to use the Sheets file for yourself, you can create copy by clicking **File -> Create a Copy**.

More info on the About sheet.

### Do you want a simple program to get you all official TCG cards?
This is the program. It downloads data from https://www.pokellector.com/sets and gains some basic information about them (prefixes like Paldean, suffixes like ex, VSTAR ...) and linking them to the individual pokemon in the pokedex. 

(When more pokemon are listed on the card - e.g. Alolan Exeggutor & Rowlet - it doesn't link the card to any pokemon).

Just run *create_from_beginning.py*.

The program outputs two files - *set_names.txt* - containing information about sets and *master.txt* containing all card informations linked to the individual set ID from the former file.

The only trouble (as far as I know) I had with Nidoran♂ and Nidoran♀. They will be bunched together and in their pokedex number, there'll be **(29f, 32m)** written and you have to distinguish between the two by yourself. Nidoran♀ (female) has No. 29 in pokedex, Nidoran♂ (male) has No. 32.

### Requirements
Python (I ran it on 3.9.13, but there really shouldn't be anything preventing it from running it in the older versions).
Other requirements are in [requirements.txt](requirements.txt) file. Just run `pip install -r requirements.txt` inside the folder.

### Known issues
Urshifu from Chilling Reign
Dolliv
Flabébé (unprintable char 'é' from web)