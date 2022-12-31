from PySide6 import QtCore, QtWidgets

from Model import PokemonModel

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_fileName = ""
        self.m_predictionModel = PokemonModel()
        self.m_selectFileButton = QtWidgets.QPushButton("Select file...")
        self.m_classifyImageButton = QtWidgets.QPushButton("Classify image")
        self.m_resultTextEdit = QtWidgets.QTextEdit()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.m_selectFileButton)
        self.layout.addWidget(self.m_classifyImageButton)
        self.layout.addWidget(self.m_resultTextEdit)

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
            self.m_resultTextEdit.clear()
            predictions = self.m_predictionModel.computePredictions(self.m_fileName)
            for pokemon, probabilty in predictions:
                self.m_resultTextEdit.append(f"{pokemon} => {probabilty}%")
        