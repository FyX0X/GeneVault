import socket
import hashlib


# packet format
# 0: owner id
# 1: token
# 2: action


IP_SERVEUR = '10.57.29.52'  # Remplacez par votre adresse IP locale
PORT = 54321

tokens = {}
file_count = {}

with open("data.csv", "r") as file:
    lines = file.readlines()
    for line in lines:
        owner_id, token, file_id = line.strip().split(",")
        tokens[owner_id] = token
        file_count[owner_id] = file_id


def check_token(owner_id, token):
    """Check if the token is valid for the given owner ID."""
    if owner_id in tokens:
        hash_token = hashlib.sha256(token.encode()).hexdigest()
        return hash_token == tokens[owner_id]
    return False

def main():
    while True:
        print("Waiting for information ...")
        packet, adclient = sserveur.recvfrom(4096)
        packet = packet.decode()
        packet = packet.split(",")
        try:
            if packet[0] == "-1":   # new owner
                owner_id = len(tokens)
                hash_token = hashlib.sha256(packet[1].encode()).hexdigest()
                tokens[owner_id] = hash_token
                file_count[owner_id] = 0
            else:
                owner_id = packet[0]
                if check_token(owner_id, packet[1]):
                    pass
            
            reponse = str(owner_id) + "," + str(owners[str(owner_id)])
            sserveur.sendto(reponse.encode(), adclient)
            print(owner_id)
            print(file_id)
        except:
            reponse = "Owner_ID doesn't exist"
            sserveur.sendto(reponse.encode(), adclient)       
        # Affichage des informations
        print(f"Data received from {adclient[1]} : {packet}")
        print(f"Owner ID: {owner_id}, File ID: {file_id}")



if __name__ == "__main__":
    sserveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sserveur.bind((IP_SERVEUR, PORT))
    print(f"Server started, waiting connection on {IP_SERVEUR}:{PORT}")
    main()
    sserveur.close()

    
