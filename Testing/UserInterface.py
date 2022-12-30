from PySide6 import QtCore, QtWidgets

from Model import PokemonModel

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_fileName = ""
        self.m_predictionModel = PokemonModel()
        self.m_selectFileButton = QtWidgets.QPushButton("Select file...")
        self.m_classifyImageButton = QtWidgets.QPushButton("Classify image")
        self.m_resultLineEdit = QtWidgets.QLineEdit()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.m_selectFileButton)
        self.layout.addWidget(self.m_classifyImageButton)
        self.layout.addWidget(self.m_resultLineEdit)

        self.m_selectFileButton.clicked.connect(self.onSelectFileButtonClicked)
        self.m_classifyImageButton.clicked.connect(self.onClassifyImageButtonClicked)

    @QtCore.Slot()
    def onSelectFileButtonClicked(self):
        fileName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self, "Please select an image", "", "Images (*.png *.jpg)")
        fileInfo = QtCore.QFileInfo(fileName)
        if fileInfo.exists() and fileInfo.isFile():
            self.m_fileName = fileName
            print(f"Selected file: {fileName}")

    @QtCore.Slot()
    def onClassifyImageButtonClicked(self):
        if self.m_fileName:
            print("Starting prediction...")
            predictedPokemon, predictionProbability = self.m_predictionModel.computePrediction(self.m_fileName)
            self.m_resultLineEdit.setText(f"{predictedPokemon} => {predictionProbability}")
        