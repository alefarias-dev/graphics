import cv2


def imgClone(filename, new_filename):
    """ Le o arquivo de imagem filename e cria uma copia em new_filename
    """
    return saveImage(f'../.temp/{new_filename}', readImage(filename))


def saveImage(filename, img):
    """ Salva a matriz img (numpy.array) em filename
    """
    cv2.imwrite(filename, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    return filename, img


def readImage(filename):
    """ Retorna a matriz RGB da imagem filename
    """
    return cv2.cvtColor(cv2.imread(filename), cv2.COLOR_BGR2RGB)
