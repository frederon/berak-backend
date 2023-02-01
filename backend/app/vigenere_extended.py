def encrypt(data, key):
    key = key.encode()
    key_len = len(key)
    key_index = 0
    encrypted_data = bytearray()
    for i in range(len(data)):
        key_byte = key[key_index % key_len]
        encrypted_data.append((data[i] + key_byte) % 256)
        key_index += 1
    return bytes(encrypted_data)


def decrypt(encrypted_data, key):
    key = key.encode()
    key_len = len(key)
    key_index = 0
    decrypted_data = bytearray()
    for i in range(len(encrypted_data)):
        key_byte = key[key_index % key_len]
        decrypted_data.append((encrypted_data[i] - key_byte) % 256)
        key_index += 1
    return bytes(decrypted_data)
