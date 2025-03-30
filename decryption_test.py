import Cryptography
import reassembler

key = b'\xbf\xd2\xd7\x1bp\xe2vq\xbe\x99\xc4,Z4\x83\xd9'
input_file = "test/img.dna"
output_file = "test/img_decrypted.jpeg"

data_list = reassembler.open_file_as_list(input_file)
data = reassembler.recombine_bytes_from_dna_strands(data_list)
data_depadded = reassembler.remove_padding(data)
print(data[-20:])
print("Data depadded:", data_depadded[-20:])

if len(data_depadded) % 16 != 0:
    print("Error: Data length is not a multiple of the AES block size!")
else:
    print("Data length is a multiple of the AES block size.")

decrypted_data = Cryptography.decrypt_file(key, data_depadded)

with open(output_file, 'wb') as f:
    f.write(decrypted_data)
print("Decrypted data written to", output_file)