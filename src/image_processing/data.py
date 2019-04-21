import matplotlib.pyplot as plt


def histograma_bandas(img):
    """ recebe uma imagem RGB (numpy.array), retorna os vetores 
    para montar o histograma das bandas
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
    return r_hist, g_hist, b_hist


def histogram(img, filename, show_log=False):
    """ recebe uma imagem RGB (numpy.array) e salva o plot dos
    histogramas no filename indicado
    """
    plt.style.use('bmh')
    r_hist, g_hist, b_hist = histograma_bandas(img)
    fig, axarr = plt.subplots(3, sharex=True, sharey=True, figsize=(4.26, 3.18))
    plt.subplots_adjust(hspace=.5)
    x = list(range(256))
    axarr[0].bar(x, height=r_hist, color='red', alpha=.64, width=1, log=True)
    axarr[0].set_title('Histograma Vermelho', fontsize=8)
    axarr[0].tick_params(axis='both', which='both', length=0)
    axarr[0].grid(False)
    axarr[1].bar(x, height=g_hist, color='green', alpha=.64, width=1, log=True)
    axarr[1].set_title('Histograma Verde', fontsize=8)
    axarr[1].tick_params(axis='both', which='both', length=0)
    axarr[1].grid(False)
    axarr[2].bar(x, height=b_hist, color='blue', alpha=.64, width=1, log=True)
    axarr[2].set_title('Histograma Azul', fontsize=8)
    axarr[2].tick_params(axis='both', which='both', length=0)
    axarr[2].grid(False)
    plt.savefig(filename)
