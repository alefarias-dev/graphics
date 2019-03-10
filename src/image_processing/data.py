import matplotlib.pyplot as plt
from io import BytesIO

def histograma_banda(img, b):
    """ recebe uma imagem e um inteiro especificando uma banda,
    retorna o vetor para montar o histograma daquela banda
    """
    banda = img[:, :, b]
    linhas, colunas = banda.shape
    hist = [0] * 256
    for linha in range(linhas):
        for coluna in range(colunas):
            hist[banda[linha, coluna]] += 1
    return hist


def histogram(r_hist, g_hist, b_hist):
    """ recebe uma img RGB e retorna
    os subplots de histogramas para cada
    banda
    """

    fig, axarr = plt.subplots(3, sharex=True)
    x = list(range(256))
    axarr[0].bar(x, height=r_hist, color='red')
    axarr[0].set_title('Histograma R')
    axarr[1].bar(x, height=g_hist, color='green')
    axarr[1].set_title('Histograma G')
    axarr[2].bar(x, height=b_hist, color='blue')
    axarr[2].set_title('Histograma B')
    
    
    image_bytes = BytesIO()
    plt.savefig(image_bytes, format='png', bbox_inches='tight', pad_inches=0)

    return image_bytes.getvalue()
