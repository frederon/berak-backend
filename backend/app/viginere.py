def encrypt(string, key):
    return "".join([chr((ord(string[i]) + ord(key[i % len(key)])) % 26 + ord('A')) for i in range(len(string))])

def decrypt(string, key):
    return "".join([chr((ord(string[i]) - ord(key[i % len(key)]) + 26) % 26 + ord('A')) for i in range(len(string))])