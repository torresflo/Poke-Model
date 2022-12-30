import requests
import random
import numpy
from io import BytesIO
import cv2

from PIL import Image
from progress.bar import ShadyBar

from selenium import webdriver
from selenium.webdriver.common.by import By

from DataCollection.PokemonData import Pokedex
from Utils.DataTools import DataSaver

import time

class PokemonSpriteCollector:
    def __init__(self, pokedex : Pokedex):
        self.m_pokedex = pokedex

    def retrieveAndSaveSprites(self):
        progressBar = ShadyBar("Retrieving Pokémon Front Sprites...", max = len(self.m_pokedex.m_data))

        for pokemonNumber, item in self.m_pokedex.m_data.items():
            progressBar.next()

            for key in {Pokedex.JsonSpriteFrontDefaultKey, Pokedex.JsonSpriteHomeFrontDefaultKey, Pokedex.JsonSpriteOfficialFrontDefaultKey}:
                url = self.m_pokedex.m_data[pokemonNumber][key]
                content = requests.get(url).content
                image = Image.open(BytesIO(content)).convert('RGBA')
                DataSaver.saveImage(image, DataSaver.DefaultTrainingDataFolderPath, pokemonNumber)

    def createFrontSpriteVariant(self, image : Image):
        backgroundColor = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        pokemonColor = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

        imageArray = numpy.array(image)
        r, g, b, a = cv2.split(imageArray)
        transparentAreas = (a == 0)
        nonTransparentAreas = (a != 0)
        imageArray[transparentAreas] = backgroundColor
        imageArray[nonTransparentAreas] = pokemonColor

        imageVariant = Image.fromarray(imageArray)
        return imageVariant
        
class BraveImageCollector:
    def __init__(self, pokedex : Pokedex):
        self.m_pokedex = pokedex
        self.m_browser = webdriver.Chrome("./DataCollection/chromedriver/chromedriver.exe")
        self.m_priorURLs = []

    def getPokemonNameFromNumber(self, pokemonNumber):
        return self.m_pokedex.m_data[pokemonNumber][Pokedex.JsonNameKey]

    def createSearchStrings(self, pokemonNumber):
        pokemonName = self.getPokemonNameFromNumber(pokemonNumber)
        texts = ['art', 'card', "wallpaper"]
        searches = []
        for text in texts:
            searches.append(f"pokemon {pokemonName} {text}".strip().replace(' ', '+'))
        return searches

    def getImagesAndTitles(self, numberOfImagesToSave):
        containers = [element for i, element in enumerate(self.m_browser.find_elements(By.CLASS_NAME, "box")) if i < numberOfImagesToSave]
        for container in containers:
            imageUrl = container.find_element(By.CLASS_NAME, "image").get_attribute("src")
            title = container.find_element(By.CLASS_NAME, "img-title").text
            yield imageUrl, title

    def trySaveImages(self, pokemonNumber, imagesURLs, titles):
        pokemonName = self.getPokemonNameFromNumber(pokemonNumber)
        for imageURL, title in zip(imagesURLs, titles):
            if pokemonName in title.lower() and imageURL not in self.m_priorURLs:
                try:
                    content = requests.get(imageURL).content
                    image = Image.open(BytesIO(content)).convert("RGBA")
                    DataSaver.saveImage(image, DataSaver.DefaultTrainingDataFolderPath, pokemonNumber)
                    self.m_priorURLs.append(imageURL)
                except:
                    continue

    def requestAndSaveImages(self, searchString, numberOfImagesToSave, pokemonNumber):
        self.m_browser.get(f"https://search.brave.com/images?q={searchString}")
        time.sleep(3) # wait the page to load
        elements = tuple(self.getImagesAndTitles(numberOfImagesToSave))
        if elements:
            imageURLs, titles = zip(*elements)
            self.trySaveImages(pokemonNumber, imageURLs, titles)
        else:
            time.sleep(30)

    def retrieveAndSaveSearchedImages(self):
        progressBar = ShadyBar("Retrieving Pokémon Images from Brave...", max = len(self.m_pokedex.m_data))

        for pokemonNumber, item in self.m_pokedex.m_data.items():
            progressBar.next()
            
            self.m_priorURLs = []
            searchStrings = self.createSearchStrings(pokemonNumber)
            numberOfImagesToSavePerSearchString = (20, 5, 5)
            for searchString, numberOfImagesToSave in zip(searchStrings, numberOfImagesToSavePerSearchString):
                self.requestAndSaveImages(searchString, numberOfImagesToSave, pokemonNumber)
