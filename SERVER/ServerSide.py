import socket
import hashlib
import os
import time

# packet format
# 0: action
# 1: owner_id
# 2: token
# 3: file

IP_SERVEUR = '10.57.29.52'  # Remplacez par votre adresse IP locale
PORT = 54321

tokens = {}
file_count = {}

def reload_csv():
    with open("SERVER/data.csv", "r") as file:
        """Fill the tokens and file_count with the exixting data"""
        lines = file.readlines()
        for line in lines:
            owner_id, token, file_id = line.strip().split(",")
            tokens[owner_id] = token
            file_count[owner_id] = int(file_id)
reload_csv()

def check_token(owner_id, token):
    """Check if the token is valid for the given owner ID."""
    if owner_id in tokens:
        hash_token = hashlib.sha256(token.encode()).hexdigest()
        return hash_token == tokens[owner_id]
    return False

def handle_client(client_socket):
    """Handles the packets sent by the client"""
    print("Waiting for information ...")
    packet = client_socket.recv(4096).decode()

    packet = packet.split(",")
    try:
        action = packet[0]
        owner_id = packet[1]
        token = packet[2] 
    except:
        pass

    if action == "read":
        """When the client ask to read his files"""
        try:
            if check_token(owner_id,token) is True:
                file = "SERVER/client_data/" + str(owner_id) + "/" + str(packet[3]) + ".dna"
                with open(file, 'r') as f:
                    reponse = f.read()    
                client_socket.sendall(str(len(reponse)).encode()) 
                Confirmation = client_socket.recv(1000000).decode()
                if Confirmation == "Ok":
                    client_socket.sendall(reponse.encode())
                print("Reading sucessful !")
            else:
                client_socket.sendall("Wrong token".encode()) 
                return   
        except Exception as e:
            client_socket.sendall("There has been an error in reading the file".encode())
            print("There has been an error in reading the file",e )
            return
    
    elif action == "write":
        """When the client wants to give a file"""
        try: 
            if check_token(owner_id,token) is True:
                reponse = str(file_count[owner_id])
                client_socket.sendall(str(file_count[owner_id]).encode())
                file_path = f"SERVER/client_data/{owner_id}/{file_count[owner_id]}.dna"
                file_data = client_socket.recv(1000000).decode()
                os.makedirs("SERVER/client_data/" + str(owner_id),exist_ok=True)
                with open(file_path, 'w') as f:
                    f.write(file_data)
                confirmation = "Ok"
                client_socket.sendall(confirmation.encode())
                with open("SERVER/data.csv",'r') as f:
                    lines = f.readlines()
                    line = lines[int(owner_id)].split(',')
                    count = int(line[2])
                    count += 1
                    lines[int(owner_id)] = f"{line[0]},{line[1]},{count} \n"
                with open("SERVER/data.csv", 'w') as f:
                    f.writelines(lines)
                print("Writing successful !")
            else:
                client_socket.sendall("Wrong token".encode())   
                return
        except Exception as e:
            client_socket.sendall("There has been an error in writing the file".encode())
            print("There has been an error in writing the file" ,e )
            return
    
    elif packet[0] == "register":
        """When the client is new"""
        try:
            with open("SERVER/data.csv", "a") as f:
                owner_id = len(tokens)
                hash_token = hashlib.sha256(token.encode()).hexdigest()
                f.write(str(owner_id)+ "," + str(hash_token) + ",0 \n")
            client_socket.sendall(str(owner_id).encode())
            print('Registering done !')
            reload_csv()
        except Exception as e:
            client_socket.sendall(str("There has been an error in registering").encode())
            print("There has been an error in registering",e)
            return

def main():
    """ Starts the server TCP """
    sserveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sserveur.bind((IP_SERVEUR, PORT))
    sserveur.listen(5)  # Permet 5 connexions en attente
    print(f"Server booted on {IP_SERVEUR}:{PORT}")
    client_socket, addr = sserveur.accept()
    while True:
        print(f"Connexion from {addr}")
        # Gérer le client dans une fonction séparée
        handle_client(client_socket)

    client_socket.close()

def run_server():
    """Restart the server if it crashes"""
    while True:
        try:
            main() 
        except Exception as e:
            print(f"Fatal error: {e}")
            print("Redémarrage du serveur")
            time.sleep(3) 

if __name__ == "__main__":
    run_server()