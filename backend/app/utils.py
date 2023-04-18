import base64
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

def convert_hex_digits_to_int_16(hex_digits):
    hex_chars = [format(x, 'x') for x in hex_digits]
    hex_str = ''.join(hex_chars)
    result = int(hex_str, 16)
    return result

def convert_str_to_base64(text):
    return base64.b64encode(text.encode('ascii')).decode('ascii')

def convert_base64_to_str(base64_str):
    return base64.b64decode(base64_str).decode('ascii')

def append_signature_to_message(message, signature):
    return f"{message}\n\n<ds>{signature}</ds>"

def extract_signature_from_message(appended):
    # Split the appended string using the signature delimiters
    parts = appended.split("\n\n<ds>", 1)
    if len(parts) != 2:
        raise ValueError("Signature not found in message or invalid format")
    message = parts[0]

    # Remove the closing </ds> tag from the signature
    signature = parts[1].rstrip("</ds>").rstrip('\u0000').rstrip('\x00')

    return message, signature