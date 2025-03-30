import writing
import Cryptography
import reassembler
import sliceur
import socket
import hashlib


IP_SERVER = '10.57.29.52'  # Adresse IP du serveur
PORT = 54321



def main(action: str, input: str = None, output_path: str = None, owner_id: int = None, key: bytes = None) -> None:
    """Main function to process the action."""
    if action in ["--write", '-w']:
        process_write(input, owner_id, key)
    elif action in ["--read", '-r']:
        process_read(output_path, owner_id, key, input)
    elif action == "--register":
        process_register()
    else:
        print("Invalid action. Use '--write' to save files in DNA format or '--read' to recover files from DNA.")
        return


def send_packet(action: str, owner: int = None, key: bytes = None, file_id=None):
    message = f"{action},{owner},"
    token = hashlib.sha256(key).hexdigest()
    message += token
    if file_id is not None:
        message += "," + str(file_id)
    print(f"send message: {message}")
    sclient.sendall(message.encode())


def send_msg_packet(msg: str):
    print(f"send message: {msg}")
    sclient.sendall(msg.encode())


def receive_packet(size: int = 4096) -> str:
    message = sclient.recv(size).decode()
    print(f"received packet: {message}")
    return message


def process_register():
    key = Cryptography.create_key()
    print(f"your key has been created, keep it safe and DO NOT share it. \n>>>{int.from_bytes(key, byteorder="big", signed=False)}")
    owner_id = -1
    send_packet("register", owner_id, key)

    new_owner_id = receive_packet()

    print(f"your new owner_id is: {new_owner_id}")



def process_write(input_path: str, owner_id: int, key: bytes) -> None:
    """Process the input file and write the DNA strands to the output file."""
    
    send_packet("write", owner_id, key)
    
    response = receive_packet()

    if response == "Wrong token":
        print(f"wrond credentials!")
        return

    file_id = int(response)

    print(f"writing to file_id: {file_id}.")

    encrypted = Cryptography.encrypt_file(key, input_path)  # Encrypt the input file
    sliced = sliceur.sliceur(encrypted, writing.DATA_SIZE)  # Slice the encrypted data into chunks

    with open(input_path + "_temp.dna", "w") as file:
        for i in range(len(sliced)):
            # Write the DNA strand with the given parameters
            # The owner_id, file_id, and index are set to 1 for this example
            # You can change them as needed
            file.write(writing.write_dna_strand(owner_id, file_id, i, sliced[i]) + "\n")
    print(f"the .dna file has been stored to {input_path + "_temp.dna"} and will be sent to the server.")

    with open(input_path + "_temp.dna", "r") as file:
        string_data = file.read()
        sclient.sendall(string_data.encode())
    
    response = receive_packet()

    if response == "Ok":
        print("file transmition successfull.")
    else:
        print("unexpected issue during transmition.")


def process_read(output_path: str, owner_id: int, key: bytes, file_id: int) -> None:
    send_packet("read", owner_id, key, file_id)

    first_packet = receive_packet()
    if first_packet == "Wrong token":
        print(f"wrond credentials!")
        return
    size = int(first_packet)
    send_msg_packet("Ok")
    data = receive_packet(size)

    write_file(output_path + "_temp.dna", data.encode())

    dna_strands = reassembler.open_file_as_list(output_path + "_temp.dna")  # Read the DNA strands from the input file
    recombined_bytes = reassembler.recombine_bytes_from_dna_strands(dna_strands)   # Create ordered DNA strands
    depadded = reassembler.remove_padding(recombined_bytes)
    decripted = Cryptography.decrypt_file(key, depadded) # Decrypt the ordered DNA data

    write_file(output_path, decripted)  # Create an empty file at the output path
    print(f"Decrypted data saved to {output_path}")


def write_file(output_path: str, data: bytes) -> None:
    """Write the decrypted data to a file."""
    with open(output_path, "wb") as file:
        file.write(data)


if __name__ == "__main__":

    sclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sclient.connect((IP_SERVER, PORT))

    print("connection established")

    
    action = input("Enter the action ('--write' or '--read' or '--register' or '--exit'): ")

    while action != '--exit':
        try:
            # Prompt for input if arguments are not provided
            if action in ['--read', '-r']:
                owner_id = int(input("Enter the Owner ID: "))
                key = int(input("Enter the encryption key: ")).to_bytes(16, byteorder="big", signed=False)  # Convert the key to bytes
                _input = input("Enter the file_id of the file you are requesting: ")
                output_path = input("Enter the path for output file: ")
            elif action in ['--write', '-w']:
                owner_id = int(input("Enter the Owner ID: "))
                key = int(input("Enter the encryption key: ")).to_bytes(16, byteorder="big", signed=False)  # Convert the key to bytes
                _input = input("Enter the path to the input file: ")
                output_path = None
            else:        
                _input = None
                output_path = None
                owner_id = None
                key = None
            main(action, _input, output_path, owner_id, key)

            action = input("Enter the action ('--write' or '--read' or '--register' or '--exit'): ")
        except socket.error as e:
            if e.errno == 10054:
                print(f"Connexion was severed, aborting the program.")
                sclient.close()
                exit()
        except Exception as e:
            print(f"Unexpected error: {e}")

        
    sclient.close()


# -------------------------------------------------------------

import socket
import hashlib
import Cryptography
import writing
import reassembler
import sliceur

IP_SERVER = '0.0.0.0'  # Listen on all interfaces
PORT = 54321
BUFFER_SIZE = 4096

# In-memory storage for registered users (Replace with persistent storage if needed)
users = {}
files = {}


def receive_packet(conn, size=BUFFER_SIZE) -> str:
    message = conn.recv(size).decode()
    print(f"Received packet: {message}")
    return message


def send_packet(conn, message: str):
    print(f"Sending message: {message}")
    conn.sendall(message.encode())


def process_register(conn):
    key = Cryptography.create_key()
    owner_id = len(users) + 1  # Assign new ID
    users[owner_id] = key
    send_packet(conn, str(owner_id))
    print(f"Registered new user: {owner_id}")


def process_write(conn, owner_id: int, key: bytes):
    if owner_id not in users or users[owner_id] != key:
        send_packet(conn, "Wrong token")
        return

    file_id = len(files) + 1  # Assign new file ID
    files[file_id] = b""
    send_packet(conn, str(file_id))

    data = receive_packet(conn, BUFFER_SIZE * 100)  # Receive large data
    files[file_id] = data.encode()
    send_packet(conn, "Ok")
    print(f"Stored file {file_id} for owner {owner_id}")


def process_read(conn, owner_id: int, key: bytes, file_id: int):
    if owner_id not in users or users[owner_id] != key:
        send_packet(conn, "Wrong token")
        return

    if file_id not in files:
        send_packet(conn, "File not found")
        return

    data = files[file_id]
    send_packet(conn, str(len(data)))
    receive_packet(conn)  # Wait for client confirmation
    conn.sendall(data)
    print(f"Sent file {file_id} to owner {owner_id}")


def handle_client(conn, addr):
    print(f"New connection from {addr}")
    while True:
        try:
            message = receive_packet(conn)
            if not message:
                break
            
            parts = message.split(",")
            action = parts[0]
            owner_id = int(parts[1]) if len(parts) > 1 else None
            key = bytes.fromhex(parts[2]) if len(parts) > 2 else None
            file_id = int(parts[3]) if len(parts) > 3 else None

            if action == "register":
                process_register(conn)
            elif action == "write":
                process_write(conn, owner_id, key)
            elif action == "read":
                process_read(conn, owner_id, key, file_id)
            else:
                send_packet(conn, "Invalid action")
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            break

    conn.close()
    print(f"Connection closed from {addr}")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((IP_SERVER, PORT))
    server.listen(5)
    print(f"Server listening on {IP_SERVER}:{PORT}")

    while True:
        conn, addr = server.accept()
        handle_client(conn, addr)


if __name__ == "__main__":
    start_server()
