def encrypt(string, key):
    return "".join([chr((ord(string[i]) + ord((key + string[:len(string)-len(key)])[i])) % 26 + ord('A')) for i in range(len(string))])

def decrypt(ciphertext, key):
    plaintext = ""
    auto_key = key
    for i in range(len(ciphertext)):
        plaintext += chr((ord(ciphertext[i]) - ord('A') - ord(auto_key[i]) - ord('A')) % 26 + ord('A'))
        auto_key += plaintext[i]
    return plaintext