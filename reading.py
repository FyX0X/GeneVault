import translator
import reedsolo
from writing import DATA_SIZE, ERROR_CORRECTION_SIZE


rs = reedsolo.RSCodec(ERROR_CORRECTION_SIZE)  # 33% error correction bytes


def read_dna_strands(dna_str: str) -> list:
    """Read the DNA strands from the given DNA string."""
    assert dna_str.startswith("ACAC") and dna_str.endswith("AGAG"), "Invalid DNA string format."

    bytes_data = translator.dna_to_bytes(dna_str[4:-4])  # Remove prefix and suffix



    owner_bytes = bytes_data[0:2]  # 2 bytes (4 pairs)
    file_bytes = bytes_data[2:4]  # 2 bytes (4 pairs)
    index_bytes = bytes_data[4:6]  # 2 bytes (4 pairs)
    encoded_data = bytes_data[6:-2]  # 108 nt (27 bytes) long (27 bytes)
    checksum = bytes_data[-2:]  # 2 bytes (4 pairs)

    print(bytes_data)
    print(checksum)

    assert verify_checksum_prime(bytes_data[:-2], checksum), "Checksum verification failed. Data may be corrupted."
    
    owner_id = int.from_bytes(owner_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    file_id = int.from_bytes(file_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    index = int.from_bytes(index_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)

    
    try:
        data = rs.decode(encoded_data)
        print(f"Decoded: {data}")
        print(f"Decoded (text): {translator.bytes_to_text(data[0])}")
    except reedsolo.ReedSolomonError as e:
        print(f"Error during decoding: {e}")

    return {
        "owner_id": owner_id,
        "file_id": file_id,
        "index": index,
        "data": data[0],  # First part of the decoded data
    }


def verify_checksum_prime(data: bytes, checksum: bytes) -> bytes:
    """Calculate the checksum by dividing the data by the largest prime that fits in 2 bytes."""
    LARGEST_PRIME = 65521  # Largest prime number that fits in 2 bytes
    
    # Calculate the checksum as the remainder of the sum of the data divided by the prime
    checksum_value = sum(data) % LARGEST_PRIME
    return checksum_value.to_bytes(2, byteorder="big", signed=False) == checksum


if __name__ == "__main__":
    # Example usage
    dna_str = "ACACAGAAAGCTAAAATGCGAAAAAAAATACATCTTTCGATCGATCGGACGAACAATTTGTCGGTGACTCGATCTAACATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGGGCAGCCAGACGAATCGGCATGGTGGAATTGATAGCCCAGCGCGTCTCCAAGACGACAGAG"
    print(read_dna_strands(dna_str))
