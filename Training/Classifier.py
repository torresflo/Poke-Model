import os
import lightning
import torch
import torch.utils.data

from PIL import Image
from transformers import ViTForImageClassification, ViTFeatureExtractor
from torch.optim import AdamW
from lightning.pytorch.callbacks import Callback

from progress.bar import ShadyBar 

from DataCollection.PokemonData import Pokedex
from Utils.DataTools import DataSaver

class PokemonClassifier(lightning.LightningModule):
    DefaultModelDataFolderPath = "./data/model"

    def __init__(self, pokedex : Pokedex):
        super().__init__()
        self.m_pokedex = pokedex

        modelName = "google/vit-base-patch16-224"
        self.m_model = ViTForImageClassification.from_pretrained(modelName)
        self.m_featureExtractor = ViTFeatureExtractor.from_pretrained(modelName)
        self.m_batchSize = 12 #Use what can fit in memory
        self.m_lr = 5e-5
        
        self.m_model.classifier = torch.nn.Linear(768, self.m_pokedex.m_maxPokemonNumber)
        self.m_model.num_labels = self.m_pokedex.m_maxPokemonNumber
        self.updateConfig()

    def updateConfig(self):
        id2Label, label2Id = {}, {}
        for pokemonNumber, item in self.m_pokedex.m_data.items():
            index = int(pokemonNumber) - 1
            pokemonName = item[Pokedex.JsonNameKey]
            id2Label[index] = pokemonName
            label2Id[pokemonName] = index

        self.m_model.config.id2label = id2Label
        self.m_model.config.label2id = label2Id

    def getDatasets(self, path):
        progressBar = ShadyBar("Loading datasets...", max = len(self.m_pokedex.m_data))

        for pokemonNumber, item in self.m_pokedex.m_data.items():
            progressBar.next()
            folderPath = f"{path}/{pokemonNumber}"
            imageNames = os.listdir(folderPath)
            for imageName in imageNames:
                imageTensor = self.m_featureExtractor(images=Image.open(f"{folderPath}/{imageName}").convert("RGB"), return_tensors="pt")
                labelTensor = torch.zeros(1, dtype=torch.long)
                labelTensor[0] = int(pokemonNumber) - 1
                yield imageTensor, labelTensor

    # Overriden methods from LightningModule
    def prepare_data(self):
        trainData = tuple(self.getDatasets(DataSaver.DefaultAugmentationDataFolderPath))
        self.m_trainDataset = torch.utils.data.random_split(trainData, [len(trainData), 0])[0]
        testData = tuple(self.getDatasets(DataSaver.DefaultTestDataFolderPath))
        self.m_testDataset = torch.utils.data.random_split(testData, [len(testData), 0])[0]

    def forward(self, batch, batch_idx):
        return self.m_model(batch[0]["pixel_values"].squeeze(), labels=batch[1].squeeze())
    
    def training_step(self, batch, batch_idx):
        loss = self(batch, batch_idx)[0]
        self.log("train_loss", loss)
        return loss

    def validation_step(self, batch, batch_idx):
        output = self(batch, batch_idx)
        predidctedLabels = output[1].argmax(-1)
        realLabels = batch[1].squeeze()
        accuracy = torch.sum(predidctedLabels == realLabels) / self.m_batchSize
        self.log("val_accuracy", accuracy)
        loss = output[0]
        self.log("val_loss", loss)

    def train_dataloader(self):
        return torch.utils.data.DataLoader(self.m_trainDataset, batch_size=self.m_batchSize, drop_last=True, shuffle=True, num_workers=0)

    def val_dataloader(self):
        return torch.utils.data.DataLoader(self.m_testDataset, batch_size=self.m_batchSize, drop_last=False, shuffle=False, num_workers=0)

    def configure_optimizers(self):
        return AdamW(self.parameters(), lr=self.m_lr, weight_decay=0.01)

class SaveCallback(Callback):
    def on_train_epoch_end(self, trainer, pl_module):
        if(pl_module.current_epoch > 0):
            currentEpoch = str(pl_module.current_epoch)
            epochFolderName= f"epoch_{currentEpoch}"
            path = f"{PokemonClassifier.DefaultModelDataFolderPath}/{epochFolderName}"
            DataSaver.createFolder(path)
            pl_module.m_model.save_pretrained(path)