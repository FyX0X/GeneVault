import socket
import hashlib
import os
import time
import csv

# packet format
# 0: action
# 1: owner_id
# 2: token
# 3: file

IP_SERVEUR = '10.57.29.52'  # Remplacez par votre adresse IP locale
PORT = 54321
SERVER_CSV_DATABASE = "SERVER/data.csv"

client_data = []
tokens = {}
file_count = {}

import csv

filename = "data.csv"

tokens = []
file_count = []

def load_csv():
    # Open the CSV file and read it as a list of dictionaries
    with open(SERVER_CSV_DATABASE, "r", newline="") as file:
        reader = csv.reader(file)  # Read CSV as dictionary

        for row in reader:
            # Append dictionary with selected fields (ignoring "id")
            tokens.append(row[1])
            file_count.append(row[2])

load_csv()

def send_packet(action: str, owner: int = None, key: bytes = None, file_id=None):
    message = f"{action},{owner},"
    token = hashlib.sha256(key).hexdigest()
    message += token
    if file_id is not None:
        message += "," + str(file_id)
    print(f"send message: {message}")
    client_socket.sendall(message.encode())


def send_msg_packet(msg: str):
    print(f"send message: {msg}")
    sclient.sendall(msg.encode())


def receive_packet(size: int = 4096) -> str:
    message = sclient.recv(size).decode()
    print(f"received packet: {message}")
    return message

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
        # Accept a new connection
        client_socket, client_address = sserveur.accept()
        print(f"Connection received from {client_address}")

        # Receive data (max 1024 bytes at a time)
        data = client_socket.recv(1024)
        if not data:
            break

        print(f"Received: {data.decode()}")

        # Send a response
        client_socket.sendall(b"Message received!")

        # Close the client connection
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