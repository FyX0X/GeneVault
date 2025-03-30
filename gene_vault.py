import argparse
import writing
import reading as reading
import Cryptography
import reassembler
import sliceur
import socket
import hashlib


IP_SERVEUR = '10.57.29.52'  # Adresse IP du serveur
PORT = 54321



def main(action: str, input_path: str, output_path: str, owner_id: int, key: bytes) -> None:
    """Main function to process the action."""
    if action == "--write":
        process_write(input_path, output_path, owner_id, key)
    elif action == "--read":
        process_read(input_path, output_path, owner_id, key)
    else:
        print("Invalid action. Use '--write' to save files in DNA format or '--read' to recover files from DNA.")
        return
    
print("Hello, welcome to the Fork project")
print("Are you a new user? [Y/N]")
user = input().upper()
if user == "N":
    owner_id = input("Owner_ID: ")
    key = input("Key: ")
elif user == "Y":
    owner_id = 1
    key = Cryptography.create_key()
    print("Your Owner_Id is " + str(owner_id) + " and your key is " + str(key) + " (Please keep them safe and do NOT share them)")
print("key", int.from_bytes(key, byteorder="big", signed=False))
print("What file do you want to put in the time capsule ?")
input_file = input("Path: ")
print("Where do you want your encrypted file ?")
output_file = input("Path: ")
print("what is the name of your file ?")
output = input("Name: ")
print("Send us the .dna file and we will store it!")


def send_packet(owner: int, key: bytes):
    message = owner
    token = hashlib.sha256(key).hexdigest()
    message += token
    sclient.sendto(message.encode(), (IP_SERVEUR, PORT))

def process_write(input_path: str, output_path: str, owner_id: int, key: bytes) -> None:
    """Process the input file and write the DNA strands to the output file."""
    writed = []
    encrypted = Cryptography.encrypt_file(key, input_path)  # Encrypt the input file
    sliced = sliceur.sliceur(encrypted, writing.DATA_SIZE)  # Slice the encrypted data into chunks

    file_id = 1  # Example file ID, you can change it as needed
    with open(output_path, "w") as file:
        for i in range(len(sliced)):
            # Write the DNA strand with the given parameters
            # The owner_id, file_id, and index are set to 1 for this example
            # You can change them as needed
            file.write(writing.write_dna_strand(owner_id, file_id, i, sliced[i]) + "\n")

    print(f"DNA strands saved to {output_path}")

    



def process_read(input_path: str, output_path: str, owner_id: int, key: bytes) -> None:
    dna_strands = reassembler.open_file_as_list(input_path)  # Read the DNA strands from the input file
    recombined_bytes = reassembler.recombine_bytes_from_dna_strands(dna_strands).rstrip(b'\x00')   # Create ordered DNA strands
    decripted = Cryptography.decrypt_file(key, recombined_bytes) # Decrypt the ordered DNA data

    write_file(output_path, decripted)  # Create an empty file at the output path
    print(f"Decrypted data saved to {output_path}")


def write_file(output_path: str, data: bytes) -> None:
    """Write the decrypted data to a file."""
    with open(output_path, "wb") as file:
        file.write(data)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Save your files in DNA format or recover files from DNA.")
    parser.add_argument("action", type=str, choices=["--write", "--read"], help="Action to perform: '--write' to save files in DNA format, '--read' to recover files from DNA.")
    parser.add_argument("input_path", type=str, nargs="?", help="Path to the input file")
    parser.add_argument("output_path", type=str, nargs="?", help="Path to save the output file")
    parser.add_argument("owner_id", type=int, nargs="?", help="Owner ID")
    parser.add_argument("key", type=int, nargs="?", help="Encryption key")
    args = parser.parse_args()

    # Prompt for input if arguments are not provided
    action = args.action or input("Enter the action ('--write' or '--read'): ")
    input_path = args.input_path or input("Enter the path to the input .dna file: ")
    output_path = args.output_path or input("Enter the path to save the output file: ")
    owner_id = args.owner_id or int(input("Enter the Owner ID: "))
    key = args.key or int(input("Enter the encryption key: ")).to_bytes(16, byteorder="big", signed=False)  # Convert the key to bytes

    
    sclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    main(action, input_path, output_path, owner_id, key)