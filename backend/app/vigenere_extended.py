def encrypt(bytes, key):
    return "".join([chr((ord(bytes[i]) + ord(key[i % len(key)])) % 256) for i in range(len(bytes))])

def decrypt(bytes, key):
    return "".join([chr((ord(bytes[i]) - ord(key[i % len(key)]) + 256) % 256) for i in range(len(bytes))])