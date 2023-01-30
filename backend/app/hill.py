import numpy as np
from . import utils

BOGUS_LETTER = 'X'

n = 26  # ukuran alfabet


def validate_key(key, m):
    key_flatten = np.array(key).flatten()

    if len(key_flatten) != m*m:
        raise Exception(f"Key matrix doesn't match m, which is {m}x{m}")


def pad_text(text, m):
    while len(text) % m != 0:
        text += BOGUS_LETTER
    return text


def encrypt(text, key, m):
    validate_key(key, m)
    text = pad_text(text, m)

    result = ''
    text_splitted = utils.split(text, m)

    try:
        inverse_matrix(key, m)
    except Exception as exc:
        raise Exception("Key matrix isn't invertible") from exc

    for group in text_splitted:
        p = [utils.char_to_int(char.upper()) for char in group]
        for i in range(m):
            c = 0
            for j in range(m):
                if j < len(p):
                    c += key[i][j] * p[j]
            c = c % n
            result += utils.int_to_char(c)

    return result


def inverse_matrix(K, m):
    det = int(np.linalg.det(K))
    det_multiplicative_inverse = pow(det, -1, 26)
    K_inv = [[0] * m for i in range(m)]
    for i in range(m):
        for j in range(m):
            Dji = K
            Dji = np.delete(Dji, (j), axis=0)
            Dji = np.delete(Dji, (i), axis=1)
            det = Dji[0][0]*Dji[1][1] - Dji[0][1]*Dji[1][0]
            K_inv[i][j] = (det_multiplicative_inverse *
                           pow(-1, i+j) * det) % 26
    return K_inv


def decrypt(text, key, m):
    validate_key(key, m)
    text = pad_text(text, m)

    key_inverse = inverse_matrix(key, m)
    result = ''
    text_splitted = utils.split(text, m)

    for group in text_splitted:
        p = [utils.char_to_int(char.upper()) for char in group]
        for i in range(m):
            c = 0
            for j in range(m):
                c += key_inverse[i][j] * p[j]
            c = c % n
            result += utils.int_to_char(c)

    return result


# print(encrypt(
#     'paymoremoney',
#     [
#       [17, 17, 5],
#       [21, 18, 21],
#       [2, 2, 19]
#       ], 3
# ))
# print(decrypt(
#     'LNSHDLEWMTRW',
#     [
#       [17, 17, 5],
#       [21, 18, 21],
#       [2, 2, 19]
#       ]
# ))
