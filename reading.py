import translator
import reedsolo
import zlib
from writing import DATA_SIZE, ERROR_CORRECTION_SIZE


rs = reedsolo.RSCodec(ERROR_CORRECTION_SIZE)  # 33% error correction bytes


verbose = False  # Set to True for verbose output


def read_dna_strands(dna_str: str) -> list:
    """Read the DNA strands from the given DNA string."""
    assert dna_str.startswith("ACAC") and dna_str.endswith("AGAG"), "Invalid DNA string format."

    bytes_data = translator.dna_to_bytes(dna_str[4:-4])  # Remove prefix and suffix

    owner_bytes = bytes_data[0:2]  # 2 bytes (4 pairs)
    file_bytes = bytes_data[2:4]  # 2 bytes (4 pairs)
    index_bytes = bytes_data[4:6]  # 2 bytes (4 pairs)
    encoded_data = bytes_data[6:-2]  # 108 nt (27 bytes) long (27 bytes)
    checksum = bytes_data[-2:]  # 2 bytes (4 pairs)

    assert verify_checksum(bytes_data[:-2], checksum), "Checksum verification failed. Data may be corrupted."
    
    owner_id = int.from_bytes(owner_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    file_id = int.from_bytes(file_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    index = int.from_bytes(index_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)

    data = rs.decode(encoded_data)  # Decode the Reed-Solomon encoded data


    if verbose:
        print(f"Decoded data: {data}")
        print(f"Owner ID: {owner_id}")
        print(f"File ID: {file_id}")
        print(f"Index: {index}")
        print(f"Checksum: {checksum}")
        print(f"Data: {translator.bytes_to_text(data[0])}")


    return {
        "owner_id": owner_id,
        "file_id": file_id,
        "index": index,
        "data": data[0],  # First part of the decoded data
    }

def verify_checksum(data: bytes, checksum: bytes) -> bool:
    """Verify the checksum of the given data."""
    cs = (zlib.crc32(data) & 0xFFFF).to_bytes(2, byteorder="big", signed=False)  # 2 bytes (8 pairs)

    return cs == checksum


if __name__ == "__main__":
    # Example usage
    dna_str = "ACACAGAAAGCTAAAATGCGAAAAAAATTACATCTTTCGATCGATCGGACGAACAATTTGTCGGTGACTCGATCTAACATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGGGCAGCCAGACGAATCGGCATGGTGGAATTGATAGCCCAGCGCGTCTCCGTCAATATAGAG"
    print(read_dna_strands(dna_str))