import re


def char_to_int(char):
    return ord(char) - ord('A')


def int_to_char(num):
    return chr(num + ord('A'))


def split(string, num):
    return [string[start:start+num] for start in range(0, len(string), num)]


def uppercase_and_filter_alphabets(string):
    string = string.upper()
    return re.sub('[^A-Z]+', '', string)
