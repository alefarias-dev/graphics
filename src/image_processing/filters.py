import numpy as np
import math
from .data import histograma_bandas


"""
Importante!

Considere a representacao da imagem como se segue:

A imagem eh uma lista de listas, cada lista interna eh uma linha
cada linha possui diferentes listas para cada pixel da imagem, a
quantidade de listas dentro de uma linha eh a quantidade de colunas
da imagem bidimensional. Logo, uma imagem toda preta seria representada
do seguinte modo:
[
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
    [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
]

A principio assuma que todos os filtros recebem uma imagem RGB
"""


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
                soma_pixel_splitting(valor, k)  # soma k em cada valor do pixel
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


"""

Implementacao de filtros

Suavizacao
- Filtro de media
- Filtro de mediana

Realce
- Filtro de quanticacao
- Filtro Splitting
- Equalizacao

"""


"""

Algoritmos de vizinhanca

- Vizinhanca de 8
- Vizinhanca de 4
- Vizinhanca diagonal

"""

def valid_positions(positions, img_shape):
    linhas, colunas, dimensoes = img_shape
    valid_positions = []
    for position in positions:
        linha, coluna = position
        if (linha < linhas and linha >= 0 and coluna < colunas and coluna > 0):
            valid_positions.append(position)
    return valid_positions


def valid_position(i, j, img_shape):
    linhas, colunas, _ = img_shape
    return (0 <= i < linhas and 0 <= j < colunas)


def neighbors_8(img, i, j, b):
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
        neighbors.append(img[linha, coluna, b])
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


def aplica_template(img, template, template_size=3):
    """Dado uma imagems e um template, aplica o template nos pixels da imagem

    Arguments:
        img {numpy.ndarray} -- Imagem onde será aplicado o template.
        template {numpy.ndarray} -- Template (N, N) que será aplicado na imagem.
    """

    if template_size == 3:
        range_start = 1
    elif template_size == 2:
        range_start = 0
    else:
        raise ValueError("Tamanho de template não suportado.")

    range_end_offset = 1

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
            img_copy[linha, coluna] = novo_valor

    return img_copy

def filtro_gradiente_horizontal(img):
    template = np.array([[-1, -1], [1, 1]])
    #template = np.array([[0, 0], [0, 0]])
    return aplica_template(img, template, template_size=2)

def filtro_gradiente_vertical(img):
    template = np.array([[-1, 1], [-1, 1]])
    return aplica_template(img, template, template_size=2)

def filtro_passa_alta(img):
    template = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
    #template = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    return aplica_template(img, template)

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
