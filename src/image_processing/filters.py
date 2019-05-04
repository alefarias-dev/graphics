import numpy as np
import math
from .data import histograma_bandas, histograma_cinza


def soma_pixel(valor_pixel, escalar):
    """ recebe um inteiro e retorna a soma
    do inteiro mais um escalar e retorna a soma
    no intervalo 0 - 255 sem estourar o intervalo
    """
    soma = valor_pixel + escalar
    if soma < 0: return 0
    if soma > 255: return 255
    return soma


def soma_pixel_splitting(valor_pixel, escalar):
    if valor_pixel > 128:
        soma = valor_pixel + escalar
    else:
        soma = valor_pixel - escalar
    if soma < 0: return 0
    if soma > 255: return 255
    return soma


def soma_escalar(img, k, splitting=False):

    if splitting:
        func_soma = soma_pixel
    else:
        func_soma = soma_pixel_splitting

    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            img[linha, coluna] = [
                func_soma(valor, k)  # soma k em cada valor do pixel
                for valor in img[linha, coluna]
            ]
    return img


def clarear(img, k):
    """ recebe uma matriz numpy representando a imagem
    e soma o escalar k em todas as posicoes
    """
    return soma_escalar(img, k)


def escurecer(img, k):
    """ recebe uma matriz numpy representando a imagem
    e subtrai o escalar k em todas as posicoes
    """
    return soma_escalar(img, -k)


def valid_positions(positions, img_shape):
    linhas, colunas = img_shape[0:2]
    valid_positions = []
    for position in positions:
        linha, coluna = position
        if (linha < linhas and linha >= 0 and coluna < colunas and coluna > 0):
            valid_positions.append(position)
    return valid_positions


def valid_position(i, j, img_shape):
    linhas, colunas = img_shape[0:2]
    return (0 <= i < linhas and 0 <= j < colunas)


def neighbors_8(img, i, j, b=None):
    """ retorna arranjo de valores dos pixeis
    na neighbors de 8
    """
    positions = [
        (i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1),
        (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1), (i, j)
    ]
    positions = valid_positions(positions, img.shape)
    neighbors = []
    for position in positions:
        linha, coluna = position
        if b: neighbors.append(img[linha, coluna, b])
        else: neighbors.append(img[linha, coluna])
    return neighbors


def neighbors_4(img, i, j, b):
    """ retorna arranjo de valores dos pixeis
    na neighbors de 4
    """
    positions = [
        (i-1, j), (i, j-1), (i, j+1), (i+1, j), (i, j)
    ]
    positions = valid_positions(positions, img.shape)
    neighbors = []
    for position in positions:
        linha, coluna = position
        neighbors.append(img[linha, coluna, b])
    return neighbors


def neighbors_diag(img, i, j, b):
    """ retorna arranjo de valores dos pixeis
    na neighbors diagonal
    """
    positions = [
        (i-1, j-1), (i-1, j+1), (i+1, j-1), (i+1, j+1), (i, j)
    ]
    positions = valid_positions(positions, img.shape)
    neighbors = []
    for position in positions:
        linha, coluna = position
        neighbors.append(img[linha, coluna, b])
    return neighbors


NEIGHBORHOOD = {
    '8': neighbors_8,
    '4': neighbors_4,
    'diag': neighbors_diag
}

def aplica_template(img, template, template_size=3, t=0, count_r=False):
    """Dado uma imagems e um template, aplica o template nos pixels da imagem

    Arguments:
        img {numpy.ndarray} -- Imagem onde sera aplicado o template.
        template {numpy.ndarray} -- Template (N, N) que sera aplicado na imagem.
        t {int} -- Valor de threshold para limitar template

    Return:
        img_coph {numpy.ndarray} -- Imagem
        counter {int} -- |R|
    """

    if template_size == 3:
        range_start = 1
    elif template_size == 2:
        range_start = 0
    else:
        raise ValueError("Tamanho de template nao suportado.")

    range_end_offset = 1
    counter = 0
    img_copy = img.copy()
    linhas, colunas = img.shape
    template_linhas, template_colunas = template.shape
    for linha in range(range_start, linhas-range_end_offset):
        for coluna in range(range_start, colunas-range_end_offset):
            novo_valor = 0
            for linha_template in range(template_linhas):
                for coluna_template in range(template_colunas):
                    novo_valor += template[linha_template, coluna_template] * \
                        img[linha + linha_template - range_start, coluna + coluna_template - range_start]

            if novo_valor < 0:
                novo_valor = 0
            elif novo_valor > 255:
                novo_valor = 255

            counter += 1 if count_r and novo_valor > t else 0
            img_copy[linha, coluna] = novo_valor if novo_valor > t else 0

    if count_r:
        return img_copy, counter
    else:
        return img_copy

def filtro_direcao_reta(img, t):
    template_horizontal = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]])
    template_vertical = np.array([[-1, 2, -1], [-1, 2, -1], [-1, 2, -1]])
    template_45 = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]])
    template_minus_45 = np.array([[2, -1, -1], [-1, 2, -1], [-1, -1, 2]])

    img_h, R_h = aplica_template(img, template_horizontal, t=t, count_r=True)
    img_v, R_v = aplica_template(img, template_vertical, t=t, count_r=True)
    img_45, R_45 = aplica_template(img, template_45, t=t, count_r=True)
    img_minus45, R_minus45 = aplica_template(img, template_minus_45, t=t, count_r=True)

    direcao = ["Horizontal", "Vertical", "45°", "-45°"]
    imgs = [img_h, img_v, img_45, img_minus45]
    R_filters = [R_h, R_v, R_45, R_minus45]
    idx_filtro = np.argmax(R_filters)

    return imgs[idx_filtro], direcao[idx_filtro]


def filtro_gradiente_horizontal(img):
    template = np.array([[-1, -1], [1, 1]])
    #template = np.array([[0, 0], [0, 0]])
    return aplica_template(img, template, template_size=2)


def filtro_gradiente_vertical(img):
    template = np.array([[-1, 1], [-1, 1]])
    return aplica_template(img, template, template_size=2)


def filtro_passa_alta(img, t):
    template = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    #template = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    return aplica_template(img, template, t=t)


def filtro_sobel(img):
    template_horizontal = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
    template_vertical = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

    img_horizontal = aplica_template(img, template_horizontal)
    img_vertical =  aplica_template(img, template_vertical)

    img_copy = img.copy()
    linhas, colunas = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            img_copy[linha, coluna] = min(int(img_horizontal[linha, coluna]) + int(img_vertical[linha, coluna]), 255)

    return img_copy


def filtro_media_fatima(img, mask_size='3'):
    img_copy = img.copy()
    l = math.floor(int(mask_size)/2)
    # TODO: implementar o filtro
    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            for b in range(dimensoes):
                soma = 0
                valid = 0
                for i in range(linha-l, linha+l+1):
                    for j in range(coluna-l, coluna+l+1):
                        if (valid_position(i, j, img.shape)):
                            valid +=1
                            soma += img[i, j, b]
                img_copy[linha, coluna, b] = math.ceil(soma/valid)
    return img_copy


def filtro_mediana_fatima(img, mask_size='3'):
    img_copy = img.copy()
    l = math.floor(int(mask_size)/2)
    # TODO: implementar o filtro
    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            for b in range(dimensoes):
                values = []
                for i in range(linha-l, linha+l+1):
                    for j in range(coluna-l, coluna+l+1):
                        if (valid_position(i, j, img.shape)):
                            values.append(img[i, j, b])
                values = sorted(values)
                if len(values) % 2 == 0:
                    a = (int(values[len(values) // 2]) + int(values[len(values) // 2 - 1]))//2
                    img_copy[linha, coluna, b] = np.uint8(a)
                else:
                    img_copy[linha, coluna, b] = values[len(values)//2]
    return img_copy


def hist_acc(v):
    return [
        sum(v[0:i])
        for i in range(1, len(v)+1)
    ]


def formula_magica(idx, hist_idx, i):
    return max(0, (hist_idx/i)-1)


def equalizar(img):
    histogramas = histograma_bandas(img)
    histogramas_acumulados = [(hist_acc(hist)) for hist in histogramas]
    linhas, colunas, dimensoes = img.shape
    i = linhas * colunas / 256

    qs = []
    for hist in range(len(histogramas_acumulados)):
        v_q = []
        for idx in range(len(histogramas_acumulados[hist])):
            v_q.append(formula_magica(idx, histogramas_acumulados[hist][idx], i))
            #print(v_q)
        qs.append(v_q)

    for linha in range(linhas):
        for coluna in range(colunas):
            for b in range(dimensoes):
                #print(qs[b])
                img[linha, coluna, b] = qs[b][img[linha, coluna, b]]

    return img


def filtro_media(img, neighbors='8'):
    neighborhood = NEIGHBORHOOD[neighbors]
    # TODO: implementar o filtro
    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            img[linha, coluna] = [
                np.mean(neighborhood(img, linha, coluna, b))
                for b in range(dimensoes)
            ]
    return img


def filtro_mediana(img, neighbors='8'):
    neighborhood = NEIGHBORHOOD[neighbors]
    # TODO: implementar o filtro
    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            img[linha, coluna] = [
                np.median(neighborhood(img, linha, coluna, b))
                for b in range(dimensoes)
            ]
    return img


def filtro_quantizacao(img, quantidade_cores):

    intervalo = 255/quantidade_cores

    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            novos_intervalos = [cor//intervalo for cor in img[linha, coluna]]
            novas_cores = [i * intervalo for i in novos_intervalos]
            img[linha, coluna] = novas_cores
    return img


def filtro_splitting(img, constante):
    return soma_escalar(img, constante, splitting=True)


def limiarizacao(img, t):
    linhas, colunas = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            img[linha, coluna] = 0 if img[linha, coluna] < t else 255
    return img

def limiar_adaptativo(img):
    hist = histograma_cinza(img)
    ponto_inflexao = get_ponto_inflexao(hist)
    return limiarizacao(img, ponto_inflexao)

def get_ponto_inflexao(h):
    anterior = h[0]
    menor_atual = float('Inf')
    ponto_inflexao = 0
    for index, value in enumerate(h[1::]):
        if value > anterior and menor_atual > anterior:
            menor_atual = anterior
            ponto_inflexao = index - 1
    return ponto_inflexao

def limiar_local(img, k):
    linhas, colunas = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            vizinhos = neighbors_8(img, linha, coluna)
            media_vizinhos = sum(vizinhos)/len(vizinhos)
            pixel = img[linha, coluna]
            t = media_vizinhos * k
            img[linha, coluna] = 255 if pixel >= t else 0
    return img
