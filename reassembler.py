import reading
import Cryptography
import argparse  # Added for CLI support

def main():
    parser = argparse.ArgumentParser(description="Reassemble DNA data from a file and output the result.")
    parser.add_argument("input_path", type=str, nargs="?", help="Path to the input .dna file")
    parser.add_argument("output_path", type=str, nargs="?", help="Path to save the output file")
    args = parser.parse_args()

    # Prompt for input if arguments are not provided
    input_path = args.input_path or input("Enter the path to the input .dna file: ")
    output_path = args.output_path or input("Enter the path to save the output file: ")

    # Add your processing logic here
    print(f"Processing input file: {input_path}")
    print(f"Output will be saved to: {output_path}")


    list_of_dna_strands = open_file(input_path)  # Read the DNA strands from the input file
    ordered_dna_data = create_ordered_dna_strands(list_of_dna_strands)  # Create ordered DNA strands

    write_file(output_path, ordered_dna_data)  # Create an empty file at the output path


def create_ordered_dna_strands(dna_strands: list[str]) -> bytes:
    """"Create ordered DNA strands from the list of DNA strands."""
    ordered_dna_strands = [None] * len(dna_strands)  # Initialize an empty list to hold the ordered DNA strands

    for strand in dna_strands:

        print(len(strand))
        strand_data = reading.read_dna_strands(strand)  # Read the DNA strands


        index = strand_data["index"]  # Get the index from the DNA strand data
        ordered_dna_strands[index] = strand_data["data"]  # Store the data at the correct index

    # Join all the ordered DNA strands into a single bytes object
    return b"".join(ordered_dna_strands)


def open_file(input_path: str) -> list[str]:
    """Open the input file and read the DNA strands."""
    with open(input_path, "r") as file:
        dna_strands = file.readlines()
    return [strand.strip() for strand in dna_strands]


def write_file(output_path: str, data: bytes) -> None:
    """Write the decrypted data to a file."""
    with open(output_path, "wb") as file:
        file.write(data)


if __name__ == "__main__":
    main()


