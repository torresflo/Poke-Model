![GitHub license](https://img.shields.io/github/license/torresflo/Poke-Model.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
![GitHub contributors](https://img.shields.io/github/contributors/torresflo/Poke-Model.svg)
![GitHub issues](https://img.shields.io/github/issues/torresflo/Poke-Model.svg)

<p align="center">
  <h1 align="center">Poké Model</h3>

  <p align="center">
    A bunch of Python scripts to create a Pokémon Classifier.
    <br />
    <a href="https://github.com/torresflo/Poke-Model/issues">Report a bug or request a feature</a>
  </p>
</p>

## Table of Contents

* [Introduction](#introduction)
* [Getting Started](#getting-started)
  * [Prerequisites and dependencies](#prerequisites-and-dependencies)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)

## Introduction

This repository is **heavily** inspired by the project <a href="https://github.com/imjeffhi4/pokemon-classifier">pokemon-classifier by imjeffhi4</a>, check it out!

The repository contains different scripts to create a Pokémon Classifier. You will find scripts to:
- Collect images of Pokémon on internet to create a dataset.
- Augment the variety of the dataset by doing random transformations to the images.
- Fine-tune a classifier with the dataset.
- Test the classifier.

## Getting Started

### Prerequisites and dependencies

This repository is tested on Python 3.7+.

You should install Poké Model in a [virtual environment](https://docs.python.org/3/library/venv.html). If you're unfamiliar with Python virtual environments, check out the [user guide](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
First, create a virtual environment with the version of Python you're going to use and activate it.

Depending of the scripts you want to execute, you need to instal various packages.

**Data Collection**

For the data collection scripts, the following packages are required :
- *selenium* is used to do search and retrieve images from the browser Chrome (you need to put the chrome driver executable in the folder `DataCollection/chromedriver`)
- *pillow* is used to load and manipulate images.
- *cv2* is used to perform transformations on images.
- *progress* is used to feedback progression with beautiful progress bars.

**Training**

For the training scripts, the following packages are required :
- *pytorch-lightning* (and *torch*) are used to manipulate the model
- *transformers* is used for the model
- *pillow* is used to load and manipulate images.
- *progress* is used to feedback progression with beautiful progress bars.

**Testing**

For the training scripts, the following packages are required :
- *PySide6* is used for the user interface
- *torch* is used to manipulate the model
- *transformers* is used for the model
- *pillow* is used to load and manipulate images.

All packages can be installed with the regular:

```bash
pip install <package-name>
```

### Installation

Follow the instructions above then clone the repo (`git clone https:://github.com/torresflo/Poke-Model.git`). 

## Usage

To start the data collection, use the script `main_collecting.py`.\
For the training of the model, use the script `main_training.py`.\
Finally, to test the generated model in a simple UI, use the script `Testing\main.py`.

The images are collected using a mixture of <a href="https://pokeapi.co/">PokeAPI</a> and images scraped from <a href="https://brave.com/fr/search/">Brave Search</a>.\
Note that Brave Search will sometimes requires a Captcha to be performed. The script will wait until it is done.

Training is performed by using <a href="https://www.pytorchlightning.ai/">PyTorch Lightning</a> and by fine-tuning a ViT-base model (`google/vit-base-patch16-224`).

### Screenshot ###

Here is a screenshot of the test program (`Testing\main.py`):

![Example image](https://raw.githubusercontent.com/torresflo/Poke-Model/main/examples/example1.png)

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- LICENSE -->
## License

Distributed under the GNU General Public License v3.0. See `LICENSE` for more information.
