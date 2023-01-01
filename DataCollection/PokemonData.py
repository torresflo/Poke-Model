import requests
import json
import os

from progress.bar import ShadyBar

from Utils.DataTools import DataSaver

class Pokedex:
    JsonNameKey = "name"
    JsonGenerationKey = "generation"
    JsonSpriteFrontDefaultKey = "sprite_front_default_url"
    JsonSpriteHomeFrontDefaultKey = "sprite_home_front_default_url"
    JsonSpriteOfficialFrontDefaultKey = "sprite_official_front_default_url"

    def __init__(self):
        self.m_data = {}
        self.m_maxPokemonNumber = 905
        self.m_defaultDataFolder = "./data"
        self.m_defaultJsonFileName = f"{self.m_defaultDataFolder}/pokemon_data.json"

    def getGeneration(self, pokemonNumber):
        if pokemonNumber <= 151:
            return 1
        elif pokemonNumber <= 251:
            return 2
        elif pokemonNumber <= 386:
            return 3
        elif pokemonNumber <= 493:
            return 4
        elif pokemonNumber <= 649:
            return 5
        elif pokemonNumber <= 721:
            return 6
        elif pokemonNumber <= 809:
            return 7
        elif pokemonNumber <= 905:
            return 8
        
        return 0

    def retrieveData(self):
        progressBar = ShadyBar("Retrieving Pokémon Data...", max = self.m_maxPokemonNumber)
            
        for pokemonNumber in range (1, self.m_maxPokemonNumber + 1):
            progressBar.next()
            
            request = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonNumber}/")
            pokemonData = json.loads(request.content)
            generation = self.getGeneration(pokemonNumber)
            self.m_data[pokemonNumber] = {
                Pokedex.JsonNameKey: pokemonData["name"],
                Pokedex.JsonGenerationKey: generation,
                Pokedex.JsonSpriteFrontDefaultKey: pokemonData["sprites"]["front_default"],
                Pokedex.JsonSpriteHomeFrontDefaultKey: pokemonData["sprites"]["other"]["home"]["front_default"],
                Pokedex.JsonSpriteOfficialFrontDefaultKey: pokemonData["sprites"]["other"]["official-artwork"]["front_default"]}

    def saveDataToJsonFile(self, jsonFileName):
        with open(jsonFileName, 'w+', encoding='utf-8') as file:
            json.dump(self.m_data, file, indent=2, ensure_ascii=False)

    def loadDataFromJsonFile(self, jsonFileName):
        with open(jsonFileName, 'r', encoding='utf-8') as file:
            self.m_data = json.load(file)

    def retrieveDataAndSaveToJson(self):
        self.retrieveData()
        DataSaver.createFolder(self.m_defaultDataFolder)
        self.saveDataToJsonFile(self.m_defaultJsonFileName)

    def autoInitialize(self):
        if os.path.exists(self.m_defaultJsonFileName):
            self.loadDataFromJsonFile(self.m_defaultJsonFileName)
        else:
            self.retrieveDataAndSaveToJson()