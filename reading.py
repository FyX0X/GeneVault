import translator
import reedsolo
from writing import DATA_SIZE, ERROR_CORRECTION_SIZE


rs = reedsolo.RSCodec(ERROR_CORRECTION_SIZE)  # 33% error correction bytes


def read_dna_strands(dna_str: str) -> list:
    """Read the DNA strands from the given DNA string."""
    assert dna_str.startswith("ACAC") and dna_str.endswith("AGAG"), "Invalid DNA string format."

    bytes_data = translator.dna_to_bytes(dna_str[4:-4])  # Remove prefix and suffix


    try:
        data = bytes(rs.decode(bytes_data)[0])
    except reedsolo.ReedSolomonError as e:
        print(f"Error during decoding: {e}")

    owner_bytes = data[0:2]  # 2 bytes (4 pairs)
    file_bytes = data[2:4]  # 2 bytes (4 pairs)
    index_bytes = data[4:6]  # 2 bytes (4 pairs)
    encoded_data = data[6:]  # 108 nt (27 bytes) long (27 bytes)

    
    owner_id = int.from_bytes(owner_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    file_id = int.from_bytes(file_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)
    index = int.from_bytes(index_bytes, byteorder="big", signed=False)  # 2 bytes (4 pairs)


    return {
        "owner_id": owner_id,
        "file_id": file_id,
        "index": index,
        "data": encoded_data,  # First part of the decoded data
    }


if __name__ == "__main__":
    # Example usage
    dna_str = "ACACAGAAAGCTAAAATGCGAAAAAAAATACATCTTTCGATCGATCGGACGAACAATTTGTCGGTGACTCGATCTAACATAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGGGGCAGCCAGACGAATCGGCATGGTGGAATTGATAGCCCAGCGCGTCTCCAAGACGACAGAG"
    print(read_dna_strands(dna_str))
