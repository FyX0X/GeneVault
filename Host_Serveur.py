import socket

# Initialisation des variables
owner_max = -1
file_id = 0

IP_SERVEUR = '10.57.29.52'  # Remplacez par votre adresse IP locale
PORT = 54321

sserveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sserveur.bind((IP_SERVEUR, PORT))

print(f"Serveur démarré, en attente de connexions sur {IP_SERVEUR}:{PORT}")
owners = {}
while True:
    print("Attente d'information ...")
    donnees, adclient = sserveur.recvfrom(4096)
    donnees = donnees.decode()
    donnees = donnees.split(",")
    try:
        new_owner = donnees[0]
        if new_owner == "True":
            owner_max +=1
            owner_id = owner_max
            owners[str(owner_id)] = 0
        elif new_owner == "False":
            owner_id = donnees[1]
            owners[str(owner_id)] += 1          
        reponse = str(owner_id) + "," + str(owners[str(owner_id)])
        sserveur.sendto(reponse.encode(), adclient)
        print(owner_id)
        print(str(owners[str(owner)]))
    except:
        reponse = "Owner_ID doesn't exist"
        sserveur.sendto(reponse.encode(), adclient)       
    # Affichage des informations
    print(f"Données reçues de {adclient[1]} : {donnees}")
    print(f"Owner ID: {owner_id}, File ID: {file_id}")

sserveur.close()

    
