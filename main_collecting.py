from DataCollection.PokemonData import Pokedex
from DataCollection.ImageCollection import PokemonSpriteCollector, BraveImageCollector
from DataCollection.ImageAugmentation import ImageAugmenter

if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.autoInitialize()
    
    spriteCollector = PokemonSpriteCollector(pokedex)
    spriteCollector.retrieveAndSaveSprites()

    braveImageCollector = BraveImageCollector(pokedex)
    braveImageCollector.retrieveAndSaveSearchedImages()

    ImageAugmenter.generateAndSaveAugmentedImages(pokedex)