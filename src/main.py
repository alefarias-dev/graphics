from image_processing.filters import clarear, escurecer
from image_processing.data import histogram


from PySide2 import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPixmap
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Computer Graphics")

        # definicao das imagens
        pixmap = QPixmap('../.temp/pardal.jpg')
        pixmap = pixmap.scaled(450, 300)
        self.imagemOriginalText = QLabel('Imagem original')
        self.imagemOriginal = QLabel()
        self.imagemOriginal.setPixmap(pixmap)
        self.imagemModificadaText = QLabel('Imagem modificada')
        self.imagemModificada = QLabel()
        self.imagemModificada.setPixmap(pixmap)

        # load and reset buttons
        self.btnLoadImage = QPushButton('Carregar imagem...')
        self.btnResetImage = QPushButton('Resetar imagem...')

        pixmap = QPixmap('../.temp/hist_original.png')
        pixmap = pixmap.scaled(450, 300)
        self.histogramaOriginal = QLabel()
        self.histogramaOriginal.setPixmap(pixmap)
        self.histogramaModificado = QLabel()
        self.histogramaModificado.setPixmap(pixmap)

        # cria group boxes
        gpClarear = QGroupBox("Filtro Clarear")
        self.escalarClarearText = QLabel("Escalar:")
        self.escalarClarear = QLineEdit()
        self.btnClarear = QPushButton('Clarear')
        vboxClarear = QVBoxLayout()
        vboxClarear.addWidget(self.escalarClarearText)
        vboxClarear.addWidget(self.escalarClarear)
        vboxClarear.addWidget(self.btnClarear)
        vboxClarear.addStretch(1)
        gpClarear.setLayout(vboxClarear)

        gpEscurecer = QGroupBox("Filtro Escurecer")
        self.escalarEscurecerText = QLabel("Escalar:")
        self.escalarEscurecer = QLineEdit()
        self.btnEscurecer = QPushButton('Escurecer')
        vboxEscurecer = QVBoxLayout()
        vboxEscurecer.addWidget(self.escalarEscurecerText)
        vboxEscurecer.addWidget(self.escalarEscurecer)
        vboxEscurecer.addWidget(self.btnEscurecer)
        vboxEscurecer.addStretch(1)
        gpEscurecer.setLayout(vboxEscurecer)

        layout = QGridLayout()
        layout.addWidget(self.imagemOriginal, 0, 0)
        layout.addWidget(self.btnLoadImage, 1, 0)
        layout.addWidget(self.histogramaOriginal, 2, 0)
        layout.addWidget(self.imagemModificada, 0, 1)
        layout.addWidget(self.btnResetImage, 1, 1)
        layout.addWidget(self.histogramaModificado, 2, 1)
        layout.addWidget(gpClarear, 3, 0)
        layout.addWidget(gpEscurecer, 3, 1)

        widget = QWidget()  # nossa widget principal
        widget.setLayout(layout)  # seta o layout a ser usado

        self.setCentralWidget(widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
