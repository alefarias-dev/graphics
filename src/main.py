import sys

from image_processing.filters import *
from image_processing.data import histogram
from util import imgClone, saveImage, readImage, toGrayScale, toRGB

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

        gpMedia = QGroupBox("Suavizacao media")
        self.vizinhancaMediaText = QLabel("Vizinhanca:")
        self.vizinhancaMedia = QLineEdit()
        self.btnSuavizacaoMedia = QPushButton('Suavizacao media')
        self.btnSuavizacaoMedia.clicked.connect(self.suavizacaoMediaWrapper)
        vboxMedia = QVBoxLayout()
        vboxMedia.addWidget(self.vizinhancaMediaText)
        vboxMedia.addWidget(self.vizinhancaMedia)
        vboxMedia.addWidget(self.btnSuavizacaoMedia)
        vboxMedia.addStretch(1)
        gpMedia.setLayout(vboxMedia)

        gpMediana = QGroupBox("Suavizacao mediana")
        self.vizinhancaMedianaText = QLabel("Vizinhanca:")
        self.vizinhancaMediana = QLineEdit()
        self.btnSuavizacaoMediana = QPushButton('Suavizacao mediana')
        self.btnSuavizacaoMediana.clicked.connect(self.suavizacaoMedianaWrapper)
        vboxMediana = QVBoxLayout()
        vboxMediana.addWidget(self.vizinhancaMedianaText)
        vboxMediana.addWidget(self.vizinhancaMediana)
        vboxMediana.addWidget(self.btnSuavizacaoMediana)
        vboxMediana.addStretch(1)
        gpMediana.setLayout(vboxMediana)

        gpSplitting = QGroupBox("Splitting")
        self.splittingText = QLabel("Valor:")
        self.escalarSplitting = QLineEdit()
        self.btnSplitting = QPushButton('Splitting')
        self.btnSplitting.clicked.connect(self.splittingWrapper)
        vboxSplitting = QVBoxLayout()
        vboxSplitting.addWidget(self.splittingText)
        vboxSplitting.addWidget(self.escalarSplitting)
        vboxSplitting.addWidget(self.btnSplitting)
        vboxSplitting.addStretch(1)
        gpSplitting.setLayout(vboxSplitting)

        gpQuantizacao = QGroupBox("Quantizacao")
        self.quantizacaoText = QLabel("Valor:")
        self.escalarQuantizacao = QLineEdit()
        self.btnQuantizacao = QPushButton('Quantizacao')
        self.btnQuantizacao.clicked.connect(self.quantizacaoWrapper)
        vboxQuantizacao = QVBoxLayout()
        vboxQuantizacao.addWidget(self.quantizacaoText)
        vboxQuantizacao.addWidget(self.escalarQuantizacao)
        vboxQuantizacao.addWidget(self.btnQuantizacao)
        vboxQuantizacao.addStretch(1)
        gpQuantizacao.setLayout(vboxQuantizacao)

        gpEqualizacao = QGroupBox("Equalizacao")
        self.btnEqualizar = QPushButton('Eu vou equalizar a sua cara')
        self.btnEqualizar.clicked.connect(self.equalizarWrapper)
        vboxEqualizacao = QVBoxLayout()
        vboxEqualizacao.addWidget(self.btnEqualizar)
        vboxEqualizacao.addStretch(1)
        gpEqualizacao.setLayout(vboxEqualizacao)

        gpGradHorizontal = QGroupBox("Gradiente Horizontal")
        self.btnGradHorizontal = QPushButton('Aplicar filtro')
        self.btnGradHorizontal.clicked.connect(self.gradHorizontalWrapper)
        vboxGradHorizontal = QVBoxLayout()
        vboxGradHorizontal.addWidget(self.btnGradHorizontal)
        vboxGradHorizontal.addStretch(1)
        gpGradHorizontal.setLayout(vboxGradHorizontal)

        gpGradVertical = QGroupBox("Gradiente Vertical")
        self.btnGradVertical = QPushButton('Aplicar filtro')
        self.btnGradVertical.clicked.connect(self.gradVerticalWrapper)
        vboxGradVertical = QVBoxLayout()
        vboxGradVertical.addWidget(self.btnGradVertical)
        vboxGradVertical.addStretch(1)
        gpGradVertical.setLayout(vboxGradVertical)

        gpPassaAlta = QGroupBox("Passa Alta")
        self.btnPassaAlta = QPushButton('Aplicar filtro')
        self.escalarPassaAlta = QLineEdit()
        self.btnPassaAlta.clicked.connect(self.passaAltaWrapper)
        vboxPassaAlta = QVBoxLayout()
        vboxPassaAlta.addWidget(self.escalarPassaAlta)
        vboxPassaAlta.addWidget(self.btnPassaAlta)
        vboxPassaAlta.addStretch(1)
        gpPassaAlta.setLayout(vboxPassaAlta)

        gpSobel = QGroupBox("Sobel vertical + horizontal")
        self.btnSobel = QPushButton('Aplicar filtro')
        self.btnSobel.clicked.connect(self.sobelWrapper)
        vboxSobel = QVBoxLayout()
        vboxSobel.addWidget(self.btnSobel)
        vboxSobel.addStretch(1)
        gpSobel.setLayout(vboxSobel)

        gpLimiar = QGroupBox("Limiarizacao")
        self.escalarLimiar = QLineEdit()
        self.btnLimiar = QPushButton('Limiar')
        self.btnLimiar.clicked.connect(self.limiarWrapper)
        vboxLimiar = QVBoxLayout()
        vboxLimiar.addWidget(self.escalarLimiar)
        vboxLimiar.addWidget(self.btnLimiar)
        vboxLimiar.addStretch(1)
        gpLimiar.setLayout(vboxLimiar)

        layout = QGridLayout()
        layout.addWidget(self.imagemOriginal, 0, 0, 1, 2)
        layout.addWidget(self.btnLoadImage, 1, 0, 1, 2)
        layout.addWidget(self.histogramaOriginal, 2, 0, 1, 2)
        layout.addWidget(self.imagemModificada, 0, 2, 1, 2)
        layout.addWidget(self.btnResetImage, 1, 2, 1, 2)
        layout.addWidget(self.histogramaModificado, 2, 2, 1, 2)

        gpLimiarAdaptativo = QGroupBox("Limiar adaptativo")
        self.btnLimiarAdaptativo = QPushButton('Aplicar filtro')
        self.btnLimiarAdaptativo.clicked.connect(self.limiarAdaptativoWrapper)
        vboxLimiarAdaptativo = QVBoxLayout()
        vboxLimiarAdaptativo.addWidget(self.btnLimiarAdaptativo)
        vboxLimiarAdaptativo.addStretch(1)
        gpLimiarAdaptativo.setLayout(vboxLimiarAdaptativo)

        gpLimiarLocal = QGroupBox("Limiar local")
        self.btnLimiarLocal = QPushButton('Aplicar filtro')
        self.escalarLimiarLocal = QLineEdit()
        self.btnLimiarLocal.clicked.connect(self.limiarLocalWrapper)
        vboxLimiarLocal = QVBoxLayout()
        vboxLimiarLocal.addWidget(self.escalarLimiarLocal)
        vboxLimiarLocal.addWidget(self.btnLimiarLocal)
        vboxLimiarLocal.addStretch(1)
        gpLimiarLocal.setLayout(vboxLimiarLocal)

        gpDirecaoReta = QGroupBox("Direcao Reta")
        self.btnDirecaoReta = QPushButton('Detectar direcao')
        self.escalarDirecaoReta = QLineEdit()
        self.btnDirecaoReta.clicked.connect(self.direcaoRetaWrapper)
        vboxDirecaoReta = QVBoxLayout()
        vboxDirecaoReta.addWidget(self.escalarDirecaoReta)
        vboxDirecaoReta.addWidget(self.btnDirecaoReta)
        vboxDirecaoReta.addStretch(1)
        gpDirecaoReta.setLayout(vboxDirecaoReta)

        # Adiciona groupbox de filtros na janela
        #layout.addWidget(gpClarear, 3, 0)
        #layout.addWidget(gpEscurecer, 3, 1)
        #layout.addWidget(gpMedia, 3, 0)
        #layout.addWidget(gpMediana, 3, 1)
        #layout.addWidget(gpEqualizacao, 4, 0, 1, 4)
        #layout.addWidget(gpSplitting, 3, 2)
        #layout.addWidget(gpQuantizacao, 3, 3)
        #layout.addWidget(gpGradHorizontal, 3, 0)
        #layout.addWidget(gpGradVertical, 3, 1)
        #layout.addWidget(gpSobel, 3, 2)
        #layout.addWidget(gpPassaAlta, 3, 3)
        layout.addWidget(gpLimiar, 3, 0)
        layout.addWidget(gpLimiarAdaptativo, 3, 1)
        layout.addWidget(gpLimiarLocal, 3, 2)
        layout.addWidget(gpPassaAlta, 3, 3)
        layout.addWidget(gpDirecaoReta, 3, 4)

        widget = QWidget()  # Widget principal
        widget.setLayout(layout)  # define o layout a ser usado
        self.setCentralWidget(widget)

    def direcaoRetaWrapper(self):
        k = float(self.escalarDirecaoReta.text())
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified, direcao = filtro_direcao_reta(modified, k)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('A linha é ' + direcao)

    def limiarLocalWrapper(self):
        k = float(self.escalarLimiarLocal.text())
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = limiar_local(modified, k)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def limiarWrapper(self):
        t = int(self.escalarLimiar.text())
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = limiarizacao(modified, t)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def limiarAdaptativoWrapper(self):
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = limiar_adaptativo(modified)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def gradHorizontalWrapper(self):
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = filtro_gradiente_horizontal(modified)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def gradVerticalWrapper(self):
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = filtro_gradiente_vertical(modified)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def passaAltaWrapper(self):
        img = readImage(FILENAMES['modified'])
        escalar = int(self.escalarPassaAlta.text())
        modified = toGrayScale(img)
        modified = filtro_passa_alta(modified, escalar)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def sobelWrapper(self):
        img = readImage(FILENAMES['modified'])
        modified = toGrayScale(img)
        modified = filtro_sobel(modified)
        modified = toRGB(modified)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def splittingWrapper(self):
        escalar = self.escalarSplitting.text()
        img = readImage(FILENAMES['modified'])
        modified = filtro_splitting(img, int(escalar))
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def quantizacaoWrapper(self):
        escalar = self.escalarQuantizacao.text()
        img = readImage(FILENAMES['modified'])
        modified = filtro_quantizacao(img, int(escalar))
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def clarearWrapper(self):
        """ Wrapper para o filtro clarear que
        chama a funcao com o input do usuario
        """
        escalar = self.escalarClarear.text()
        img = readImage(FILENAMES['modified'])
        modified = clarear(img, int(escalar))
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def equalizarWrapper(self):
        img = readImage(FILENAMES['modified'])
        modified = equalizar(img)
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

    def suavizacaoMediaWrapper(self):
        vizinhanca = self.vizinhancaMedia.text()
        img = readImage(FILENAMES['modified'])
        modified = filtro_media_fatima  (img, vizinhanca)
        self.updateModifiedImage(modified)
        self.messageBox('Filtro aplicado!')

    def suavizacaoMedianaWrapper(self):
        vizinhanca = self.vizinhancaMediana.text()
        img = readImage(FILENAMES['modified'])
        modified = filtro_mediana_fatima(img, vizinhanca)
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
        new_filename, img = imgClone(filename, 'original.png')
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
