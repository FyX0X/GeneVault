import translator
import reedsolo


DATA_SIZE = 27  # 108 nt (204 bits) long (27 bytes)
ERROR_CORRECTION_SIZE = 13  # 52 nt (104 bits) long (13 bytes)
rs = reedsolo.RSCodec(ERROR_CORRECTION_SIZE)  # 33% error correction bytes


def write_dna_strand(owner_id: int, file_id: int, index: int, data: bytes) -> str:
    """ Write the DNA string with the given parameters.
    args:
        owner_id (int): The ID of the owner.
        file_id (int): The ID of the file.
        index (int): The index of the data.
        data (bytes): The data to be written (must be 108 nt).
    """
    # Check if the data is 100 nt (200 bits) long
    assert len(data) == DATA_SIZE, "Data must be 108 nt (27 bytes) long."
    assert isinstance(data, bytes), "Data must be of type bytes."
    assert isinstance(owner_id, int), "Owner ID must be of type int."
    assert isinstance(file_id, int), "File ID must be of type int."
    assert isinstance(index, int), "Index must be of type int."
    assert 0 <= owner_id <= 65535, "Owner ID must be between 0 and 65535."
    assert 0 <= file_id <= 65535, "File ID must be between 0 and 65535."
    assert 0 <= index <= 65535, "Index must be between 0 and 65535."

    owner_bytes = owner_id.to_bytes(2, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    file_bytes = file_id.to_bytes(2, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    index_bytes = index.to_bytes(2, byteorder="big", signed=False)  # 2 bytes (4 pairs)


    adn_str = prefix(owner_bytes, file_bytes, index_bytes)

    rs_encoded = reedsolo_encode(data)
    adn_str += translator.bytes_to_dna(rs_encoded)  # Add Reed-Solomon encoded data to the ADN string

    cs = checksum_prime(owner_bytes, file_bytes, index_bytes, data)  # Calculate checksum of the data and ECC
    adn_str += translator.bytes_to_dna(cs)  # Add checksum to the ADN string

    adn_str += suffix()  # Add suffix to the ADN string

    return adn_str


def prefix(owner_id: bytes, file_id: bytes, index: bytes) -> str:
    """ Creates the prefix for the ADN string.
    The prefix consists of a fixed header and the owner ID, file ID, and index."""
    prefix = "ACAC" # start 4 pairs (1 byte)
    prefix += translator.bytes_to_dna(owner_id) # owner id 2 bytes
    prefix += translator.bytes_to_dna(file_id) # file id 2 bytes
    prefix += translator.bytes_to_dna(index) # index 2 bytes
    return prefix


def suffix() -> str:
    return "AGAG" # end 4 pairs (1 byte)


def reedsolo_encode(data: bytes) -> str:
    """ Write the data to the ADN string."
    The data is Reed-Solomon encoded and then converted to DNA.
    The data must be 108 nt (27 bytes) long.
    """

    # Encode data using Reed-Solomon
    encoded_data = rs.encode(data)


    return encoded_data


def checksum_prime(owner: bytes, file: bytes, index: bytes, encoded_data: bytes) -> bytes:
    """Calculate the checksum by dividing the data by the largest prime that fits in 2 bytes."""
    LARGEST_PRIME = 65521  # Largest prime number that fits in 2 bytes
    data = owner + file + index + encoded_data
    
    # Calculate the checksum as the remainder of the sum of the data divided by the prime
    checksum_value = sum(data) % LARGEST_PRIME
    return checksum_value.to_bytes(2, byteorder="big", signed=False)


if __name__ == "__main__":
    # Example usage
    owner_id = 12345
    file_id = 123
    index = 0
    data = b"Hello, World!"
    padded = data.ljust(DATA_SIZE, b'\x00')  # Pad the data to 80 nt (160 bits)

    result = write_dna_strand(owner_id, file_id, index, padded)
    dna_bytes = translator.dna_to_bytes(result)

    print("len:", len(result))
    print("len dna bytes:", len(dna_bytes))
    print(result)
    print("Owner ID:", int.from_bytes(dna_bytes[1:3], byteorder="big", signed=False))
    print("File ID:", int.from_bytes(dna_bytes[3:5], byteorder="big", signed=False))
    print("Index:", int.from_bytes(dna_bytes[5:7], byteorder="big", signed=False))
    print("Data RS_encoded:", dna_bytes[7:-3])

    try:
        decoded = rs.decode(dna_bytes[7:-3])
        print(f"Decoded: {decoded}")
        print(f"Decoded (text): {translator.bytes_to_text(decoded[0])}")
    except reedsolo.ReedSolomonError as e:
        print(f"Error during decoding: {e}")
    print("Data (text):", translator.bytes_to_text(dna_bytes[7:-3]))
    print("Checksum:", dna_bytes[-3:-1])
    print("Checksum (int):", int.from_bytes(dna_bytes[-4:], byteorder="big", signed=False))
