import os

from PIL import Image

from PokemonData import Pokedex

class ImageSaver:
    DefaultTrainingDataFolderPath = "./data/training_data/"

    def createFolder(folderName):
        if not os.path.isdir(folderName):
            os.mkdir(folderName)

    def updatePokedexImagesCount(pokedex : Pokedex, pokemonNumber, keyName):
        if keyName:
            imagesNumber = pokedex.m_data[pokemonNumber][keyName]
            pokedex.m_data[pokemonNumber][keyName] += 1
            return imagesNumber
        else:
            return ''

    def saveImage(image : Image, saveDirectory, pokedex : Pokedex, pokemonNumber, keyName):
        ImageSaver.createFolder(saveDirectory)
        imagesNumber = ImageSaver.updatePokedexImagesCount(pokedex, pokemonNumber, keyName)
        resizedImage = image.resize((224, 224))
        resizedImage.save(f"./{saveDirectory}/{pokemonNumber}_{imagesNumber}.png")