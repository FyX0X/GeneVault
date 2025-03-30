import socket

IP_SERVEUR = '10.57.29.52'  # Adresse IP du serveur
PORT = 54321

new_owner = input("Are you a new owner ? [y/n]")

if new_owner == "y":
    new_owner = True
    owner_id = -1
else:
    new_owner = False
    owner_id = input("Entrez l'ID du propriétaire : ")
    
message = f"{new_owner},{owner_id}"  # Message à envoyer au serveur

# Mon ip est 130.104.120.255
# Création du socket UDP
sclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sclient.sendto(message.encode(), (IP_SERVEUR, PORT))  # Envoi du message

print(f"Message envoyé à {IP_SERVEUR}:{PORT}")

reponse, adserveur = sclient.recvfrom(4096)  # Réception de la réponse
reponse = reponse.decode()  # Décodage de la réponse

sclient.close()

print(f"Réponse du serveur : {reponse}")