from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os 

def create_key():
    return os.urandom(16)

def encrypt_file(key, input_file, output_file):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as f:
        data = f.read()
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt_file(key, input_file, output_file):
    cipher = AES.new(key, AES.MODE_ECB)
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    
# Example usage
key = create_key()
encrypt_file(key, 'File.txt', 'EncryptedFile.txt')
decrypt_file(key, 'EncryptedFile.txt', 'DecryptedFile.xt')
