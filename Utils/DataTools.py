import os

from PIL import Image

class DataSaver:
    DefaultTrainingDataFolderPath = "./data/training_data"
    DefaultAugmentationDataFolderPath = "./data/augmentation_data"
    DefaultTestDataFolderPath = "./data/test_data"

    def createFolder(folderName):
        if not os.path.isdir(folderName):
            os.makedirs(folderName, exist_ok=True)

    def getImageNumber(folderName):
        listOfFiles = os.listdir(folderName)
        return len(listOfFiles) + 1

    def saveImage(image : Image, saveDirectory, pokemonNumber):
        DataSaver.createFolder(saveDirectory)
        DataSaver.createFolder(f"./{saveDirectory}/{pokemonNumber}")
        imagesNumber = DataSaver.getImageNumber(f"./{saveDirectory}/{pokemonNumber}")
        resizedImage = image.resize((224, 224))
        resizedImage.save(f"./{saveDirectory}/{pokemonNumber}/{imagesNumber}.png")