import Cryptography
import translator 
import writing
import sliceur


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
print("What file do you want to put in the time capsule ?")
input_file = input("Path: ")
print("Where do you want your encrypted file ?")
output_file = input("Path: ")
print("what is the name of your file ?")
output = input("Name: ")
print("Send us the .dna file and we will store it!")

path = input_file
writed = []
encrypted = Cryptography.encrypt_file(key,path)
sliced = sliceur.sliceur(encrypted, 27)
for i in range(len(sliced)):
    # Write the DNA strand with the given parameters
    # The owner_id, file_id, and index are set to 1 for this example
    # You can change them as needed
    writed.append( writing.write_dna_strand(1, 1, i, sliced[i]))
with open (output, "w")as file:
    for i in writed:
        file.write(i)
        file.write("\n")

    