import Cryptography 
import writing
import sliceur


key = b'\xbf\xd2\xd7\x1bp\xe2vq\xbe\x99\xc4,Z4\x83\xd9'
print(str(key))
print("key", int.from_bytes(key, byteorder="big", signed=False))
print("What file do you want to put in the time capsule ?")
input_file = "test/img.jpg"
output_file = "test/img.dna"
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
with open (output_file, "w")as file:
    for i in writed:
        file.write(i)
        file.write("\n")

    