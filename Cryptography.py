import os 
import numpy as np

def createkey():
    key = os.urandom(16) 
    return key

def NERM_encrypting(key, file): 
    matrix_key = np.array(list(key)).reshape(4,4)
    det_key = np.linalg.det(matrix_key)
    crypted_data = []
    with open(file, 'rb') as f:
        data = f.read()
    if len(data)%16 != 0:
        data += b'\x00' * (16 - len(data) % 16) 
    for i in range(len(data)//16):
        liste = data[(i*16):((i*16)+16)]
        matrix = np.array(list(liste), dtype=np.uint8).reshape(4,4)
        print(matrix)
        matrix = det_key*matrix
        matrix = matrix @ matrix_key
        for i in range(4):
            for j in range(4):
                crypted_data.append(matrix[i][j].tobytes())
    return crypted_data



def NERM_decrypting(key, crypted_data):
    decrypted_data = []
    matrix_key = np.array(list(key)).reshape(4,4)
    matrix_key_inv = np.linalg.inv(matrix_key)
    det_key = np.linalg.det(matrix_key)
    for i in range(len(crypted_data)//16):
        liste = crypted_data[(i*16):((i*16)+16)]
        matrix = np.array(list(liste), dtype= np.uint8).reshape(4,4)
        matrix = matrix @ matrix_key_inv
        matrix = matrix / det_key
        for i in range(4):
            for j in range(4):
                decrypted_data.append(matrix[i][j].tobytes())
    with open(decrypted_file, 'wb') as f:
        f.write(decrypted_data)
    return

key = createkey()
NERM_decrypting(key, NERM_encrypting(key,"File.txt"))
