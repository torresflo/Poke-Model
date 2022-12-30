import sys
from PySide6 import QtWidgets

from UserInterface import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    mainWindow = MainWindow()
    mainWindow.setWindowTitle("Pokemon Classifier")
    mainWindow.show()

    sys.exit(app.exec())
