def char_to_int(char):
    return ord(char) - ord('A')

def int_to_char(num):
    return chr(num + ord('A'))

def split(str, num):
    return [str[start:start+num] for start in range(0, len(str), num)]