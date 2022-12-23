from PokemonData import Pokedex
from ImageCollector import PokemonSpriteCollector, BraveImageCollector

import time

if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.autoInitialize()
    
    spriteCollector = PokemonSpriteCollector(pokedex)
    spriteCollector.retrieveAndSaveSprites()

    # braveImageCollector = BraveImageCollector(pokedex)
    # braveImageCollector.retrieveAndSaveSearchedImages()

    exit()
