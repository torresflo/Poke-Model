import os

from PIL import Image

from PokemonData import Pokedex

class ImageSaver:
    DefaultTrainingDataFolderPath = "./data/training_data"
    DefaultAugmentationDataFolderPath = "./data/augmentation_data"

    def createFolder(folderName):
        if not os.path.isdir(folderName):
            os.mkdir(folderName)

    def getImageNumber(folderName):
        listOfFiles = os.listdir(folderName)
        return len(listOfFiles) + 1

    def saveImage(image : Image, saveDirectory, pokemonNumber):
        ImageSaver.createFolder(saveDirectory)
        ImageSaver.createFolder(f"./{saveDirectory}/{pokemonNumber}")
        imagesNumber = ImageSaver.getImageNumber(f"./{saveDirectory}/{pokemonNumber}")
        resizedImage = image.resize((224, 224))
        resizedImage.save(f"./{saveDirectory}/{pokemonNumber}/{imagesNumber}.png")