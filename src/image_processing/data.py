import matplotlib.pyplot as plt


def histograma_bandas(img):
    """ recebe uma imagem e um inteiro especificando uma banda,
    retorna o vetor para montar o histograma daquela banda
    """
    linhas, colunas, _ = img.shape
    r_hist = [0] * 256
    g_hist = [0] * 256
    b_hist = [0] * 256
    for linha in range(linhas):
        for coluna in range(colunas):
            r_hist[img[linha, coluna, 0]] += 1
            g_hist[img[linha, coluna, 1]] += 1
            b_hist[img[linha, coluna, 2]] += 1
    return normalize(r_hist), normalize(g_hist), normalize(b_hist)


def normalize(values):
    return values


def histogram(img, filename):
    """ recebe uma img RGB e retorna
    os subplots de histogramas para cada
    banda
    """
    r_hist, g_hist, b_hist = histograma_bandas(img)
    fig, axarr = plt.subplots(3, sharex=True, figsize=(4.26, 3.18))
    plt.subplots_adjust(hspace=.5)
    x = list(range(256))
    axarr[0].bar(x, height=r_hist, color='red')
    axarr[0].set_title('Histograma Vermelho', fontsize=8)
    axarr[1].bar(x, height=g_hist, color='green')
    axarr[1].set_title('Histograma Verde', fontsize=8)
    axarr[2].bar(x, height=b_hist, color='blue')
    axarr[2].set_title('Histograma Azul', fontsize=8)
    plt.savefig(filename)
