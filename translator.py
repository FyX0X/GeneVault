
DNA_ALPHABET = "ATCG"
DNA_ALPHABET_REVERSE = {char: index for index, char in enumerate(DNA_ALPHABET)}

DNA_PAIRS = {
    "A": "T",
    "T": "A",
    "C": "G",
    "G": "C"
}



def write(filename: str, crypto_method: str, data: str) -> str:
    output = ""
    output += "AAAA"


def text_to_bytes(text: str) -> bytes:
    """Convert a string to bytes using UTF-8 encoding."""
    binary = bytes(text, "utf-8")
    return binary

def bytes_to_text(input_bytes: bytes) -> str:
    """Convert bytes back to string using UTF-8 decoding."""
    text = input_bytes.decode("utf-8", errors="ignore")

    return text


def bytes_to_dna(input_byte: bytes) -> str:
    """Convert bytes to DNA representation."""
    binary_str = ''.join(format(byte, '08b') for byte in input_byte)
    if len(binary_str) % 2 != 0:
        binary_str = '0' + binary_str
    
    # Convert every two binary digits to base-4
    base4_str = ''.join(str(int(binary_str[i:i+2], 2)) for i in range(0, len(binary_str), 2))

    # Convert to DNA representation

    dna_str = ''.join(DNA_ALPHABET[int(digit)] for digit in base4_str)

    return dna_str


def dna_to_bytes(dna_str: str) -> bytes:
    """Convert DNA representation back to bytes."""
    # Convert DNA to base-4
    base4_str = ''.join(str(DNA_ALPHABET_REVERSE[char]) for char in dna_str)

    # Convert base-4 to binary string
    binary_str = ''.join(format(int(digit), '02b') for digit in base4_str)

    # Pad binary string to be a multiple of 8 bits
    if len(binary_str) % 8 != 0:
        binary_str = binary_str.lstrip('0')
    
    # Convert binary string to bytes
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_array.append(int(binary_str[i:i+8], 2))
    
    return bytes(byte_array)


def dna_to_text(dna_str: str) -> str:
    """Convert DNA representation to text."""
    # Convert DNA to bytes
    byte_array = dna_to_bytes(dna_str)
    
    # Convert bytes to text
    text = bytes_to_text(byte_array)
    
    return text


def text_to_dna(text: str) -> str:
    """Convert text to DNA representation."""
    # Convert text to bytes
    byte_array = text_to_bytes(text)
    
    # Convert bytes to DNA
    dna_str = bytes_to_dna(byte_array)
    
    return dna_str
    
    

if __name__ == "__main__":


    print(bytes_to_dna(b"Hello World!"))
    print(dna_to_bytes("TACATCTTTCGATCGATCGGACAATTTGTCGGTGACTCGATCTAACAT"))

    print(dna_to_bytes("TAATTAAT"))
    print(bytes_to_text(dna_to_bytes("TAATTAAT")))

    print(text_to_dna('''{
  "owner":"-----",
  "crypto":"NERM",
  "filename":"name.txt",  
  "data":"---"
}'''))
    
    print(dna_to_text("TGCGAACCACAAACAAACACTCGGTGTGTCGCTCTTTGACACACAGCCACACACGTACGTACGTACGTACGTACACACGAAACCACAAACAAACACTCAGTGACTGCTTGAATGTATCGGACACAGCCACACTAGCTATTTTACTAGTACACACGAAACCACAAACAAACACTCTCTCCTTCGATCTTTCGCTCATTCGTTCTTACACAGCCACACTCGCTCATTCGTTCTTACGCTGTATGCATGTAACACACGAACAAACAAAACCACAAACAAACACTCTATCATTGTATCATACACAGCCACACACGTACGTACGTACACAACCTGGT"))