from PokemonData import Pokedex
from ImageCollection import PokemonSpriteCollector, BraveImageCollector
from ImageAugmentation import ImageAugmenter

if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.autoInitialize()
    
    spriteCollector = PokemonSpriteCollector(pokedex)
    spriteCollector.retrieveAndSaveSprites()

    braveImageCollector = BraveImageCollector(pokedex)
    braveImageCollector.retrieveAndSaveSearchedImages()

    ImageAugmenter.generateAndSaveAugmentedImages(pokedex)