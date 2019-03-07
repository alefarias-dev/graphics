import matplotlib.pyplot as plt


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


def histogram(img, filename):
    """ recebe uma img RGB e retorna
    os subplots de histogramas para cada
    banda
    """
    r_hist = histograma_banda(img, 0)
    g_hist = histograma_banda(img, 1)
    b_hist = histograma_banda(img, 2)
    fig, axarr = plt.subplots(3, sharex=True)
    x = list(range(256))
    axarr[0].bar(x, height=r_hist, color='red')
    axarr[0].set_title('Histograma R')
    axarr[1].bar(x, height=g_hist, color='green')
    axarr[1].set_title('Histograma G')
    axarr[2].bar(x, height=b_hist, color='blue')
    axarr[2].set_title('Histograma B')
    plt.savefig(filename)
