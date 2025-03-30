import socket

IP_SERVEUR = '10.57.29.52'  # Adresse IP du serveur
PORT = 54321
print(f"IP_SERVEUR : {IP_SERVEUR}")

    
with open("test/img.dna", 'r')as file:
    string = file.read()



    l = len(string)
    chunk_size = (l + 19) // 20  # Ensure all data is sent even if l % 20 != 0


sclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sclient.settimeout(2)  # Timeout for response

for i in range(20):
    message = string[i * chunk_size : (i + 1) * chunk_size]

    sclient.sendto(message.encode(), (IP_SERVEUR, PORT))  # Envoi du message

    print(f"Message envoyé à {IP_SERVEUR}:{PORT}")



sclient.close()
