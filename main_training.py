import lightning
from lightning.pytorch.loggers import TensorBoardLogger

from DataCollection.PokemonData import Pokedex
from Training.Classifier import PokemonClassifier, SaveCallback

if __name__ == "__main__":
    pokedex = Pokedex()
    pokedex.autoInitialize()

    pokemonModel = PokemonClassifier(pokedex)
    trainer = lightning.Trainer(
        accumulate_grad_batches=4,
        precision="bf16",
        default_root_dir="logs",
        gpus=-1,
        max_epochs=6,
        callbacks=[SaveCallback()],
        val_check_interval=0.1,
        logger=TensorBoardLogger("logs/", name='vit_with_augmentation', version=0)
    )
    trainer.fit(pokemonModel)