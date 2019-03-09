import cv2


def img2Temp(filename):
    """ Recebe o endereco de uma imagem
    e salva a imagem na pasta temp do projeto
    retorna endereco da imagem e imagem em RGB
    """
    img = cv2.imread(filename)
    filename = filename.split('/')[-1]
    extension = filename.split('.')[-1]
    new_filename = f'../.temp/original.png'
    cv2.imwrite(new_filename, img)
    return new_filename, cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def imgClone(filename, new_filename):
    img = cv2.imread(filename)
    cv2.imwrite(f'../.temp/{new_filename}', img)
    return new_filename, cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
