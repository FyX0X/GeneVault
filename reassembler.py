import reading as reading
import Cryptography
import argparse  # Added for CLI support


def recombine_bytes_from_dna_strands(dna_strands: list[str]) -> bytes:
    """"Create ordered DNA strands from the list of DNA strands."""
    bytes_list = [None] * len(dna_strands)  # Initialize an empty list to hold the ordered DNA strands

    for strand in dna_strands:

        strand_data = reading.read_dna_strands(strand)  # Read the DNA strands
        index = strand_data["index"]  # Get the index from the DNA strand data
        bytes_list[index] = strand_data["data"]  # Store the data at the correct index

    # Join all the ordered DNA strands into a single bytes object
    return b"".join(bytes_list)


def open_file_as_list(input_path: str) -> list[str]:
    """Open the input file and read the DNA strands."""
    with open(input_path, "r") as file:
        dna_strands = file.readlines()
    return [strand.strip() for strand in dna_strands]


def remove_padding(data: bytes) -> bytes:
    """Remove padding from the decrypted data."""
    return data.rstrip(b'\x00')  # Remove padding bytes (0x00) from the end of the data

