from PySide6 import QtCore, QtWidgets, QtGui

from Model import PokemonModel

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_fileName = ""
        self.m_predictionModel = PokemonModel()
        self.m_selectFileButton = QtWidgets.QPushButton("Select image...")
        self.m_selectedImageLabel = QtWidgets.QLabel("Please select an image.")
        self.m_classifyImageButton = QtWidgets.QPushButton("Classify image")
        self.m_resultTextEdit = QtWidgets.QTextEdit()

        self.m_selectedImageLabel.setMaximumHeight(300)
        self.m_resultTextEdit.setMaximumHeight(6 * self.m_resultTextEdit.fontMetrics().lineSpacing())

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.m_selectFileButton)
        self.layout.addWidget(self.m_selectedImageLabel)
        self.layout.addWidget(self.m_classifyImageButton)
        self.layout.addWidget(self.m_resultTextEdit)
        self.layout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)

        self.m_selectFileButton.clicked.connect(self.onSelectFileButtonClicked)
        self.m_classifyImageButton.clicked.connect(self.onClassifyImageButtonClicked)

    @QtCore.Slot()
    def onSelectFileButtonClicked(self):
        fileName, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(self, "Please select an image", "", "Images (*.png *.jpg)")
        fileInfo = QtCore.QFileInfo(fileName)
        if fileInfo.exists() and fileInfo.isFile():
            self.m_fileName = fileName
            pixmap = QtGui.QPixmap(fileName).scaledToHeight(self.m_selectedImageLabel.maximumHeight())
            self.m_selectedImageLabel.setPixmap(pixmap)

    @QtCore.Slot()
    def onClassifyImageButtonClicked(self):
        if self.m_fileName:
            self.m_resultTextEdit.clear()
            predictions = self.m_predictionModel.computePredictions(self.m_fileName)
            for pokemon, probabilty in predictions:
                self.m_resultTextEdit.append(f"{pokemon} => {probabilty}%")
        