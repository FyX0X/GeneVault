import translator
from reedsolo import RSCodec
import zlib


DATA_SIZE = 40  # 80 nt (160 bits) long (40 bytes)


def write_dna_strand(owner_id: int, file_id: int, index: int, data: bytes) -> str:
    """ Write the DNA string with the given parameters.
    args:
        owner_id (int): The ID of the owner.
        file_id (int): The ID of the file.
        index (int): The index of the data.
        data (bytes): The data to be written (must be 80 nt (160 bits)).
    """
    # Check if the data is 100 nt (200 bits) long
    assert len(data) == DATA_SIZE, "Data must be 80 nt (160 bits) long."
    assert isinstance(data, bytes), "Data must be of type bytes."
    assert isinstance(owner_id, int), "Owner ID must be of type int."
    assert isinstance(file_id, int), "File ID must be of type int."
    assert isinstance(index, int), "Index must be of type int."
    assert 0 <= owner_id <= 65535, "Owner ID must be between 0 and 65535."
    assert 0 <= file_id <= 65535, "File ID must be between 0 and 65535."
    assert 0 <= index <= 65535, "Index must be between 0 and 65535."

    adn_str = write_prefix(owner_id, file_id, index)

    rs_encoded = reedsolo_encode(data)

    adn_str += translator.bytes_to_dna(rs_encoded)  # Add Reed-Solomon encoded data to the ADN string


    cs = checksum_crc32(rs_encoded)  # Calculate checksum of the data and ECC

    adn_str += translator.bytes_to_dna(cs)  # Add checksum to the ADN string

    return adn_str


def write_prefix(owner_id: int, file_id: int, index: int) -> str:
    """ Write the prefix for the ADN string.
    The prefix consists of a fixed header and the owner ID, file ID, and index."""
    output = "ACACACAC" # start 8 pairs (16 bits)
    output += translator.bytes_to_dna(owner_id.to_bytes(2, byteorder="big", signed=False)) # owner id 2 bytes
    output += translator.bytes_to_dna(file_id.to_bytes(2, byteorder="big", signed=False)) # file id 2 bytes
    output += translator.bytes_to_dna(index.to_bytes(2, byteorder="big", signed=False)) # index 2 bytes
    return output

def write_data(data: bytes) -> str:
    """ Write the data to the ADN string."
    The data is Reed-Solomon encoded and then converted to DNA.
    The data must be 80 nt (160 bits) long.
    """


    # write data to dna
    output_chunks = []
    for i in range(0, len(data), 2):
        chunk = data[i:i + 2] if i + 1 < len(data) else data[i:i + 1]
        output_chunks.append(translator.bytes_to_dna(chunk))

    output = "".join(output_chunks)  # Join list into a single string

    return output


def reedsolo_encode(data: bytes) -> str:
    """ Write the data to the ADN string."
    The data is Reed-Solomon encoded and then converted to DNA.
    The data must be 80 nt (160 bits) long.
    """
    # Check if the data is 100 nt (200 bits) long
    assert len(data) == DATA_SIZE, "Data must be 80 nt (160 bits) long."
    assert isinstance(data, bytes), "Data must be of type bytes."

    # Encode data using Reed-Solomon
    rs = RSCodec(DATA_SIZE//2)  # 33% error correction bytes
    encoded_data = rs.encode(data)

    print("len encoded_data:", len(encoded_data))
    print("len(data):", len(data))

    return encoded_data


def checksum_crc32(data: bytes) -> bytes:
    """ Calculate the CRC32 checksum of the data.
    The data must be 80 nt (160 bits) long.
    """
    cs = (zlib.crc32(data) & 0xFFFFFFFF).to_bytes(4, byteorder="big", signed=False)  # 4 bytes (32 bits)
    print("len cs:", len(cs))
    print("cs:", cs)
    return cs


if __name__ == "__main__":
    # Example usage
    owner_id = 12345
    file_id = 123
    index = 1
    data = b"Hello, World!"
    padded = data.ljust(DATA_SIZE, b'\x00')  # Pad the data to 80 nt (160 bits)

    result = write_dna_strand(owner_id, file_id, index, padded)
    dna_bytes = translator.dna_to_bytes(result)

    print("len:", len(result))
    print("len dna bytes:", len(dna_bytes))
    print(result)
    print("Owner ID:", int.from_bytes(dna_bytes[2:4], byteorder="big", signed=False))
    print("File ID:", int.from_bytes(dna_bytes[4:6], byteorder="big", signed=False))
    print("Index:", int.from_bytes(dna_bytes[6:8], byteorder="big", signed=False))
    print("Data:", dna_bytes[8:-4])
    print("Data (text):", translator.bytes_to_text(dna_bytes[8:-4]))
    print("Checksum:", dna_bytes[-4:])
    print("Checksum (int):", int.from_bytes(dna_bytes[-4:], byteorder="big", signed=False))