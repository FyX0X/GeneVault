from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os 

def create_key():
    """ Creates a random key 16 bytes long"""
    return os.urandom(16)

def encrypt_file(key, input_file, encrypted_file):
    """Encrypts input_file with AES-256 CBC mode
    Args:
    input_file is a .txt file 
    output_file is a .txt file filled with bytes"""
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv  # Generate IV
    with open(input_file, 'rb') as f:
        data = f.read()
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    with open(encrypted_file, 'wb') as f:
        f.write(iv + encrypted_data)  # Save IV + ciphertext

def decrypt_file(key, encrypted_file, output_file):
    """Decrypts input_file with AES-256 CBC mode
    Args:
    input_file is a .txt file filled with bytes, an encrypted file
    output_file is a .txt fiel with the decrypted data"""
    with open(encrypted_file, 'rb') as f:
        iv = f.read(16)  # Read the first 16 bytes (IV)
        encrypted_data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)
    
# Example usage
key = create_key()
encrypt_file(key, 'File.txt', 'EncryptedFile.txt')
decrypt_file(key, 'EncryptedFile.txt', 'DecryptedFile.xt')
