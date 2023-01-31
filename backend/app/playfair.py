import numpy as np
import re
from . import utils

BOGUS_LETTER = 'X'
ALPHABETS = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'


def generate_key(text):
    text = text.upper()
    text = re.sub('[^A-Z]+', '', text)
    text = text.replace("J", "")
    text = "".join(dict.fromkeys(text))
    for i in ALPHABETS:
        if i not in text:
            text += i
    return [
        [text[(i * 5) + j] for j in range(5)]
        for i in range(5)
    ]


def construct_key_mapping(key):
    return {
        key[i][j]: [i, j]
        for i in range(5)
        for j in range(5)
    }


def validate_key(key):
    key_flatten = np.array(key).flatten()

    if len(key_flatten) != 25:
        raise Exception("Key matrix is not 5x5")
    if len(set(key_flatten)) != 25:
        raise Exception("Key matrix contains duplicate characters")


def add_bogus_letters(text):
    for i in range(len(text) - 1):
        if text[i] == text[i+1]:
            text = text[:i+1] + BOGUS_LETTER + text[i+1:]
    if len(text) % 2 == 1:
        text += BOGUS_LETTER
    return text


def encrypt(text, key):
    validate_key(key)

    result = ''

    text = text.upper()
    text = text.replace("J", "I")
    text = add_bogus_letters(text)

    mapping = construct_key_mapping(key)

    text_splitted = utils.split(text, 2)

    for group in text_splitted:
        group = group.upper()
        first_index = mapping[group[0]]
        last_index = mapping[group[1]]

        if first_index[0] == last_index[0]:  # same row
            row = first_index[0]
            result += key[row][(first_index[1] + 1) % 5]
            result += key[row][(last_index[1] + 1) % 5]
        elif first_index[1] == last_index[1]:  # same column
            col = first_index[1]
            result += key[(first_index[0] + 1) % 5][col]
            result += key[(last_index[0] + 1) % 5][col]
        else:
            result += key[first_index[0]][last_index[1]]
            result += key[last_index[0]][first_index[1]]

    return result


def revert_bogul_letters(text):
    if text[len(text) - 1] == BOGUS_LETTER and len(text) % 2 == 0:
        text = text[:-1]

    start_index = 0
    while (i := text.find(BOGUS_LETTER, start_index)) >= 0:
        if i-1 >= 0 and i+1 < len(text) and text[i-1] == text[i+1]:
            text = text[:i] + text[i+1:]
        start_index = i + 1

    return text


def decrypt(text, key):
    validate_key(key)

    result = ''

    text = text.upper()

    mapping = construct_key_mapping(key)

    text_splitted = utils.split(text, 2)

    for group in text_splitted:
        group = group.upper()
        first_index = mapping[group[0]]
        last_index = mapping[group[1]]

        if first_index[0] == last_index[0]:  # same row
            row = first_index[0]
            col = first_index[1] - 1
            col = 4 if col < 0 else col
            result += key[row][col]
            col = last_index[1] - 1
            col = 4 if col < 0 else col
            result += key[row][col]
        elif first_index[1] == last_index[1]:  # same column
            col = first_index[1]
            row = first_index[0] - 1
            row = 4 if row < 0 else row
            result += key[row][col]
            row = last_index[0] - 1
            row = 4 if row < 0 else row
            result += key[row][col]
        else:
            result += key[first_index[0]][last_index[1]]
            result += key[last_index[0]][first_index[1]]

    result = revert_bogul_letters(result)

    return result


# print(encrypt(
#     'instrumentsz',
#     [
#       ['M', 'O', 'N', 'A', 'R'],
#       ['C', 'H', 'Y', 'B', 'D'],
#       ['E', 'F', 'G', 'I', 'K'],
#       ['L', 'P', 'Q', 'S', 'T'],
#       ['U', 'V', 'W', 'X', 'Z']
#       ]
# ))
# print(decrypt(
#     'GATLMZCLRQTX',
#     [
#       ['M', 'O', 'N', 'A', 'R'],
#       ['C', 'H', 'Y', 'B', 'D'],
#       ['E', 'F', 'G', 'I', 'K'],
#       ['L', 'P', 'Q', 'S', 'T'],
#       ['U', 'V', 'W', 'X', 'Z']
#       ]
# ))
# print(encrypt(
#     'helloe',
#     [
#       ['M', 'O', 'N', 'A', 'R'],
#       ['C', 'H', 'Y', 'B', 'D'],
#       ['E', 'F', 'G', 'I', 'K'],
#       ['L', 'P', 'Q', 'S', 'T'],
#       ['U', 'V', 'W', 'X', 'Z']
#       ]
# ))
# print(decrypt(
#     'CFSUPMIU',
#     [
#       ['M', 'O', 'N', 'A', 'R'],
#       ['C', 'H', 'Y', 'B', 'D'],
#       ['E', 'F', 'G', 'I', 'K'],
#       ['L', 'P', 'Q', 'S', 'T'],
#       ['U', 'V', 'W', 'X', 'Z']
#       ]
# ))
# print(encrypt(
#     'temuiibunantimalam',
#     [
#       ['A', 'L', 'N', 'G', 'E'],
#       ['S', 'H', 'P', 'U', 'B'],
#       ['C', 'D', 'F', 'I', 'K'],
#       ['M', 'O', 'Q', 'R', 'T'],
#       ['V', 'W', 'X', 'Y', 'Z']
#       ]
# ))
