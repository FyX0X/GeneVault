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
    encrypted_data = iv + encrypted_data
    return encrypted_data

def decrypt_file(key, encrypted_data):
    """Decrypts encrypted_file with AES-256 CBC mode
    Args:
    encrypted_data is a list filled with bytes"""
    iv = encrypted_data[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data[16:]), AES.block_size)
    
    return decrypted_data
    
if __name__ == "__main__":
    key = create_key()
    liste=decrypt_file(key, encrypt_file(key, 'test/test.txt'))
    with open("test/test.txt", 'wb') as f:
        f.write(liste)
