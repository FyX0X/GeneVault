from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import os

#Génération d'une clé AES-256 et d'un IV 
def generate_key_iv():
    key = get_random_bytes(32)  # Clé AES-256 (32 octets)
    iv = get_random_bytes(16)   # IV (16 octets)
    return key, iv

#Fonction pour chiffrer un fichier avec AES-256-CBC
def encrypt_file(input_file, output_file, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))  # Padding pour un multiple de 16

    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)  # On stocke l'IV au début du fichier

    print(f"✅ Fichier chiffré enregistré sous {output_file}")

#Fonction pour déchiffrer un fichier avec AES-256-CBC
def decrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # Lire l'IV stocké au début du fichier
        ciphertext = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_file, 'wb') as f:
        f.write(plaintext)

    print(f"✅ Fichier déchiffré enregistré sous {output_file}")

#Exemple d'utilisation
key, iv = generate_key_iv()  # Génération de la clé et de l'IV

encrypt_file("mon_fichier.txt", "fichier_chiffre.aes", key, iv)  
decrypt_file("fichier_chiffre.aes", "fichier_dechiffre.txt", key)
