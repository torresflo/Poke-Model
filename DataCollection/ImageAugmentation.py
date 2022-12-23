import os
import numpy
import random
import cv2

from PIL import Image, ImageOps, ImageFilter
from progress.bar import ShadyBar

from PokemonData import Pokedex
from DataTools import ImageSaver

class ImageAugmenter:
    def quantizeImage(image : Image, amount):
        red = (numpy.asarray(image)[:, :, 0] >> amount) << amount
        green = (numpy.asarray(image)[:, :, 1] >> amount) << amount
        blue = (numpy.asarray(image)[:, :, 2] >> amount) << amount
        resultArray = numpy.stack((red, green, blue), axis=2)
        return Image.fromarray(resultArray)

    def noiseImage(image : Image):
        randomFloat = random.randint(20, 70) / 100
        array = numpy.array(image)
        gaussian = numpy.random.normal(0, randomFloat, array.size)
        gaussian = gaussian.reshape(
            array.shape[0], array.shape[1], array.shape[2]).astype("uint8")
        return Image.fromarray(cv2.add(array, gaussian))

    def cropImage(image : Image):
        left = random.randint(10, 30)
        right = random.randint(150, 200)
        top = random.randint(0, 40)
        bottom = random.randint(85, 200)
        resizedImage = image.resize((224, 224))
        return resizedImage.crop((left, top, right, bottom)).resize((224, 224))

    def getImageWithRandomAugmentation(image : Image, priorAugmentation = False):
        randomNumber = random.randint(1, 6) if not priorAugmentation else random.randint(2, 5)
        if randomNumber == 1:
            augmentedImage = ImageOps.mirror(image)
        elif randomNumber == 2:
            gaussianBlurRadius = random.randint(1, 5)
            augmentedImage = image.filter(ImageFilter.GaussianBlur(radius=gaussianBlurRadius))
        elif randomNumber == 3:
            randomDegree = random.randint(1, 359)
            augmentedImage = image.rotate(randomDegree)
        elif randomNumber == 4:
            randomShiftAmount = random.randint(4, 7)
            augmentedImage = ImageAugmenter.quantizeImage(image, randomShiftAmount)
        elif randomNumber == 5:
            augmentedImage = ImageAugmenter.noiseImage(image)
        elif randomNumber == 6:
            augmentedImage = ImageAugmenter.cropImage(image)

        if random.random() < 0.2:
            return ImageAugmenter.getImageWithRandomAugmentation(augmentedImage, True)
        return augmentedImage

    def generateAndSaveAugmentedImages(pokedex : Pokedex):
        progressBar = ShadyBar("Generate augmented images...", max = len(pokedex.m_data))

        for pokemonNumber, item in pokedex.m_data.items():
            progressBar.next()

            trainingDataFolder = f"{ImageSaver.DefaultTrainingDataFolderPath}/{pokemonNumber}"
            augmentationDataFolder = f"{ImageSaver.DefaultAugmentationDataFolderPath}/{pokemonNumber}"
            listOfImagesToAugment = os.listdir(trainingDataFolder)

            for imageName in listOfImagesToAugment:
                imagePath = f"{ImageSaver.DefaultTrainingDataFolderPath}/{pokemonNumber}/{imageName}"
                ImageSaver.saveImage(Image.open(imagePath), ImageSaver.DefaultAugmentationDataFolderPath, pokemonNumber)

            for i in range(200):
                randomImageIndex = random.randint(0, len(listOfImagesToAugment) - 1)
                randomImagePath = f"{ImageSaver.DefaultTrainingDataFolderPath}/{pokemonNumber}/{listOfImagesToAugment[randomImageIndex]}"
                augmentedImage = ImageAugmenter.getImageWithRandomAugmentation(Image.open(randomImagePath))
                ImageSaver.saveImage(augmentedImage, ImageSaver.DefaultAugmentationDataFolderPath, pokemonNumber)

