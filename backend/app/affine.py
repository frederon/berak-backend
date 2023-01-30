from . import utils

n = 26  # ukuran alfabet


def encrypt(text, m, b):
    result = ''
    for char in text:
        p = utils.char_to_int(char.upper())
        c = (m * p + b) % n
        result += utils.int_to_char(c)
    return result


def decrypt(text, m, b):
    result = ''
    for char in text:
        c = utils.char_to_int(char.upper())
        p = (c - b) * pow(m, -1, n) % n
        result += utils.int_to_char(p)
    return result


# print(encrypt('kripto', 7, 10))
# print(decrypt('czolne', 7, 10))
