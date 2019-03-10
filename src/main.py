from image_processing.filters import clarear, escurecer
from image_processing.data import histogram

from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QPixmap, QPicture, QImage, QColor
import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Computer Graphics")

        # definicao das imagens
        self.imagemOriginal = QImage('../.temp/pardal.jpg')
        self.imagemModificada = self.imagemOriginal.copy()
        pixmap = QPixmap(self.imagemOriginal)
        pixmap = pixmap.scaled(450, 300)
        self.imagemOriginalText = QLabel('Imagem original')
        self.lbImagemOriginal = QLabel()
        self.lbImagemOriginal.setPixmap(pixmap)
        self.imagemModificadaText = QLabel('Imagem modificada')
        self.lbImagemModificada = QLabel()
        self.lbImagemModificada.setPixmap(pixmap)

        # load and reset buttons
        self.btnLoadImage = QPushButton('&Carregar imagem...')
        self.btnLoadImage.clicked.connect(self.load_image)
        self.btnResetImage = QPushButton('&Resetar imagem...')
        self.btnResetImage.clicked.connect(self.reset_image)

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
        self.btnClarear.clicked.connect(self.clarear)
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
        self.btnEscurecer.clicked.connect(self.escurecer)
        vboxEscurecer = QVBoxLayout()
        vboxEscurecer.addWidget(self.escalarEscurecerText)
        vboxEscurecer.addWidget(self.escalarEscurecer)
        vboxEscurecer.addWidget(self.btnEscurecer)
        vboxEscurecer.addStretch(1)
        gpEscurecer.setLayout(vboxEscurecer)

        layout = QGridLayout()
        layout.addWidget(self.lbImagemOriginal, 0, 0)
        layout.addWidget(self.btnLoadImage, 1, 0)
        layout.addWidget(self.histogramaOriginal, 2, 0)
        layout.addWidget(self.lbImagemModificada, 0, 1)
        layout.addWidget(self.btnResetImage, 1, 1)
        layout.addWidget(self.histogramaModificado, 2, 1)
        layout.addWidget(gpClarear, 3, 0)
        layout.addWidget(gpEscurecer, 3, 1)

        widget = QWidget()  # nossa widget principal
        widget.setLayout(layout)  # seta o layout a ser usado

        self.setCentralWidget(widget)

        self.atualiza_histograma()

    def load_image(self):
        image_path = QFileDialog.getOpenFileName(title="Open Image", filter="Image Files (*.png *.jpg *.bmp)")[0]
        #print(dir(QFileDialog.Option.HideNameFilterDetails))
        if image_path != "":
            self.imagemOriginal = QImage(image_path)
            pixmap = QPixmap(self.imagemOriginal)
            pixmap = pixmap.scaled(450, 300)
            self.lbImagemOriginal.setPixmap(pixmap)
            self.reset_image()

        self.atualiza_histograma()
            
    def reset_image(self):
        self.imagemModificada = self.imagemOriginal.copy()
        self.lbImagemModificada.setPixmap(self.lbImagemOriginal.pixmap())

    def clarear(self):
        self.soma_escalar(abs(int(self.escalarClarear.text())))

    def escurecer(self):
        self.soma_escalar(-abs(int(self.escalarEscurecer.text())))

    def soma_escalar(self, valor):

        for col in range(self.imagemModificada.height()):
            for row in range(self.imagemModificada.width()):
                pixel = self.imagemModificada.pixelColor(row, col)

                red = min(pixel.red() + valor, 255) if pixel.red() + valor > 0 else 0
                green = min(pixel.green() + valor, 255) if pixel.green() + valor > 0 else 0
                blue = min(pixel.blue() + valor, 255) if pixel.blue() + valor > 0 else 0

                newPixel = QColor.fromRgb(red, green, blue)
                self.imagemModificada.setPixelColor(row, col, newPixel) 

        pixmap = QPixmap(self.imagemModificada)
        pixmap = pixmap.scaled(450, 300)
        self.lbImagemModificada.setPixmap(pixmap)

    def atualiza_histograma(self):
        rgb_original = self.count_color(self.imagemOriginal)
        rgb_modificada = self.count_color(self.imagemModificada)

        bytes_hist_original = histogram(*rgb_original)
        bytes_hist_modificado = histogram(*rgb_modificada)

        hist_original = QImage()
        hist_original.loadFromData(bytes_hist_original)
        hist_modificado = QImage()
        hist_modificado.loadFromData(bytes_hist_original)

        pixmap_original = QPixmap(hist_original)
        pixmap_original = pixmap_original.scaled(450, 300)
        self.histogramaOriginal.setPixmap(pixmap_original)
        pixmap_modificado = QPixmap(hist_modificado)
        pixmap_modificado = pixmap_modificado.scaled(450, 300)
        self.histogramaModificado.setPixmap(pixmap_modificado)     
        
    def count_color(self, image):
        r = [0]*256
        g = [0]*256
        b = [0]*256

        for col in range(image.height()):
            for row in range(image.width()):
                pixel = image.pixelColor(row, col)
                r[pixel.red()] += 1
                g[pixel.green()] += 1
                b[pixel.blue()] += 1

        return (r, g, b)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
