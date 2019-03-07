"""
Importante!

Considere a representacao da imagem como se segue
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

Assuma que todos os filtros recebem uma imagem RGB
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


def soma_escalar(img, k):
    nova_img = img.copy()
    linhas, colunas, dimensoes = img.shape
    for linha in range(linhas):
        for coluna in range(colunas):
            nova_img[linha, coluna] = [
                soma_pixel(valor, k) 
                for valor in nova_img[linha, coluna]
            ]
    return nova_img


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
