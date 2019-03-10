import cv2


def img2Temp(filename):
    """ Recebe o endereco de uma imagem
    e salva a imagem na pasta temp do projeto
    retorna endereco da imagem e imagem em RGB
    """
    img = readImage(filename)
    new_filename = f'../.temp/original.png'
    return saveImage(new_filename, img)


def imgClone(filename, new_filename):
    return saveImage(f'../.temp/{new_filename}', readImage(filename))


def saveImage(filename, img):
    cv2.imwrite(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return filename, img


def readImage(filename):
    return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
