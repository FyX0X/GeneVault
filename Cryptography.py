from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os 

def create_key():
    """ Creates a random key 16 bytes long"""
    return os.urandom(16)

def encrypt_file(key, input_file):
    """Encrypts input_file with AES-256 CBC mode
    Args:
    input_file is a .txt file"""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Generate IV
    with open(input_file, 'rb') as f:
        data = f.read()
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    return encrypted_data

def decrypt_file(key, encrypted_data):
    """Decrypts encrypted_file with AES-256 CBC mode
    Args:
    encrypted_data is a list filled with bytes"""
    with open(encrypted_file, 'rb') as f:
        iv = f.read(16)  # Read the first 16 bytes (IV)
        encrypted_data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data
    
if __name__ == "__main__":
    key = create_key()
    encrypt_file(key, 'File.txt', 'EncryptedFile.txt')
    decrypt_file(key, 'EncryptedFile.txt', 'DecryptedFile.xt')
