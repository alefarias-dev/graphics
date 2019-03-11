import sys

from image_processing.filters import clarear, escurecer
from image_processing.data import histogram
from util import img2Temp, imgClone, saveImage, readImage

from PySide2 import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import QPixmap


# arquivos utilizados para salvar imagens e histogramas
IMG_SCALE = (426, 326)
FILENAMES = {
    'original':'../.temp/original.png',
    'modified': '../.temp/modified.png',
    'hist_original': '../.temp/hist_original.png',
    'hist_modified': '../.temp/hist_modified.png'
}


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Computer Graphics")
        self.originalFilename = ""

        # Elementos para imagem original
        pixmap = QPixmap(FILENAMES['original'])
        pixmap = pixmap.scaled(*IMG_SCALE)
        self.imagemOriginalText = QLabel('Imagem original')
        self.imagemOriginal = QLabel()
        self.imagemOriginal.setPixmap(pixmap)

        # Elementos para imagem modificada
        pixmap = QPixmap(FILENAMES['modified'])
        pixmap = pixmap.scaled(*IMG_SCALE)
        self.imagemModificadaText = QLabel('Imagem modificada')
        self.imagemModificada = QLabel()
        self.imagemModificada.setPixmap(pixmap)

        # Botoes para carregar e resetar imagem
        self.btnLoadImage = QPushButton('Carregar imagem...')
        self.btnLoadImage.clicked.connect(self.openImage)
        self.btnResetImage = QPushButton('Resetar imagem')
        self.btnResetImage.clicked.connect(self.resetModifiedImage)

        # Elementos para o histograma original
        pixmap = QPixmap(FILENAMES['hist_original'])
        pixmap = pixmap.scaled(*IMG_SCALE)
        self.histogramaOriginal = QLabel()
        self.histogramaOriginal.setPixmap(pixmap)

        # Elementos para o histograma modificado
        pixmap = QPixmap(FILENAMES['hist_modified'])
        pixmap = pixmap.scaled(*IMG_SCALE)
        self.histogramaModificado = QLabel()
        self.histogramaModificado.setPixmap(pixmap)

        # Groupbox do filtro clarear
        gpClarear = QGroupBox("Filtro Clarear")
        self.escalarClarearText = QLabel("Escalar:")
        self.escalarClarear = QLineEdit()
        self.btnClarear = QPushButton('Clarear')
        self.btnClarear.clicked.connect(self.clarearWrapper)
        vboxClarear = QVBoxLayout()
        vboxClarear.addWidget(self.escalarClarearText)
        vboxClarear.addWidget(self.escalarClarear)
        vboxClarear.addWidget(self.btnClarear)
        vboxClarear.addStretch(1)
        gpClarear.setLayout(vboxClarear)

        # Groupbox do filtro escurecer
        gpEscurecer = QGroupBox("Filtro Escurecer")
        self.escalarEscurecerText = QLabel("Escalar:")
        self.escalarEscurecer = QLineEdit()
        self.btnEscurecer = QPushButton('Escurecer')
        self.btnEscurecer.clicked.connect(self.escurecerWrapper)
        vboxEscurecer = QVBoxLayout()
        vboxEscurecer.addWidget(self.escalarEscurecerText)
        vboxEscurecer.addWidget(self.escalarEscurecer)
        vboxEscurecer.addWidget(self.btnEscurecer)
        vboxEscurecer.addStretch(1)
        gpEscurecer.setLayout(vboxEscurecer)

        # Definicoes do layout da janela
        layout = QGridLayout()
        layout.addWidget(self.imagemOriginal, 0, 0)
        layout.addWidget(self.btnLoadImage, 1, 0)
        layout.addWidget(self.histogramaOriginal, 2, 0)
        layout.addWidget(self.imagemModificada, 0, 1)
        layout.addWidget(self.btnResetImage, 1, 1)
        layout.addWidget(self.histogramaModificado, 2, 1)

        # Adiciona groupbox de filtros na janela
        layout.addWidget(gpClarear, 3, 0)
        layout.addWidget(gpEscurecer, 3, 1)

        widget = QWidget()  # Widget principal
        widget.setLayout(layout)  # define o layout a ser usado
        self.setCentralWidget(widget)

    def clarearWrapper(self):
        """ Wrapper para o filtro clarear que
        chama a funcao com o input do usuario
        """
        escalar = self.escalarClarear.text()
        img = readImage(FILENAMES['modified'])
        modified = clarear(img, int(escalar))
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def escurecerWrapper(self):
        """ Wrapper para o filtro escurecer que
        chama a funcao com o input do usuario
        """
        escalar = self.escalarEscurecer.text()
        img = readImage(FILENAMES['modified'])
        modified = escurecer(img, int(escalar))
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def openImage(self):
        """ Funcao que abre uma caixa de dialogo
        para selecao de imagem
        """
        dialog = QFileDialog()
        dialog.setNameFilter('Images (*.png *.xpm *.jpg)')
        filename, _ = dialog.getOpenFileName()
        self.loadImage(filename)

    def loadImage(self, filename):
        """ Funcao para carregar a imagem no 
        pixmap da imagem original
        """
        self.originalFilename = filename
        new_filename, img = img2Temp(filename)
        pixmap = QPixmap(new_filename).scaled(*IMG_SCALE)
        self.imagemOriginal.setPixmap(pixmap)
        self.updateHistogram('hist_original', img)
        self.updateModifiedImage(img)
        self.messageBox('Imagem carregada!')

    def updateModifiedImage(self, img):
        """ Atualiza a imagem modificada para a imagem
        passada pelo parametro img (numpy.array)
        """
        saveImage(FILENAMES['modified'], img)
        pixmap = QPixmap(FILENAMES['modified']).scaled(*IMG_SCALE)
        self.imagemModificada.setPixmap(pixmap)
        self.updateHistogram('hist_modified', img)

    def resetModifiedImage(self):
        """ Desfaz as tranformacoes aplicadas na imagem modificada,
        retornando para o estado da imagem original
        """
       self.updateModifiedImage(readImage(FILENAMES['original']))
       self.messageBox('Imagem restaurada!')

    def updateHistogram(self, which, img):
        """ Atualiza o histograma de uma imagem,
        o parametro which indica se eh da imagem original
        ou da imagem modificada
        """
        filename = FILENAMES[which]
        histogram(img, filename, show_log=True)
        pixmap = QPixmap(filename).scaled(*IMG_SCALE)
        if which == 'hist_original':
            self.histogramaOriginal.setPixmap(pixmap)
            return
        self.histogramaModificado.setPixmap(pixmap)

    def messageBox(self, message):
        """ Exibe uma caixa de mensagens para o usuario
        com a mensagem passada por parametro
        """
        msgBox = QMessageBox().information(self, "Informativo", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
