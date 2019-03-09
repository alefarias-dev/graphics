import cv2


def img2Temp(filename):
    """ Recebe o endereco de uma imagem
    e salva a imagem na pasta temp do projeto
    """
    img = cv2.imread(filename)
    filename = filename.split('/')[-1]
    extension = filename.split('.')[-1]
    new_filename = f'../.temp/original.{extension}'
    cv2.imwrite(new_filename, img)
    return new_filename
