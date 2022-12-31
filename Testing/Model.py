import torch
from PIL import Image
from transformers import ViTFeatureExtractor, ViTForImageClassification

class PokemonModel:
    def __init__(self):
        self.m_device = "cuda" if torch.cuda.is_available() else "cpu"

        print("Loading model...")
        self.m_featureExtractor = ViTFeatureExtractor.from_pretrained('google/vit-base-patch16-224')
        self.m_model = ViTForImageClassification.from_pretrained('./data/model/epoch_5').to(self.m_device)
        print("Model loaded")

    def computePredictions(self, fileName, maxNumberOfPredictions=5):
        with Image.open(fileName).convert("RGB") as image:
            inputs = self.m_featureExtractor(images=image, return_tensors="pt").to(self.m_device)
            outputs = self.m_model(**inputs)
            logits = outputs.logits.softmax(dim=1)
                
            topPredictedProbabilites, topPredictedClasses = torch.topk(logits, maxNumberOfPredictions)
            topPredictedClasses = topPredictedClasses[0].tolist()
            topPredictedProbabilites = topPredictedProbabilites[0].tolist()

            predictions = []
            for predictedClass, predictedProbability in zip(topPredictedClasses, topPredictedProbabilites):
                predictedPokemon = self.m_model.config.id2label[predictedClass]
                predictions.append([predictedPokemon, round(predictedProbability * 100, 2)])
            
            return predictions