
ADN_ALPHABET = "ATCG"
ADN_ALPHABET_REVERSE = {char: index for index, char in enumerate(ADN_ALPHABET)}

ADN_PAIRS = {
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
    text = input_bytes.decode("utf-8")
    return text


def bytes_to_adn(input_byte: bytes) -> str:
    """Convert bytes to ADN representation."""
    binary_str = ''.join(format(byte, '08b') for byte in input_byte)
    if len(binary_str) % 2 != 0:
        binary_str = '0' + binary_str
    
    # Convert every two binary digits to base-4
    base4_str = ''.join(str(int(binary_str[i:i+2], 2)) for i in range(0, len(binary_str), 2))

    # Convert to ADN representation

    adn_str = ''.join(ADN_ALPHABET[int(digit)] for digit in base4_str)

    return adn_str


def adn_to_bytes(adn_str: str) -> bytes:
    """Convert ADN representation back to bytes."""
    # Convert ADN to base-4
    base4_str = ''.join(str(ADN_ALPHABET_REVERSE[char]) for char in adn_str)

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


def adn_to_text(adn_str: str) -> str:
    """Convert ADN representation to text."""
    # Convert ADN to bytes
    byte_array = adn_to_bytes(adn_str)
    
    # Convert bytes to text
    text = bytes_to_text(byte_array)
    
    return text


def text_to_adn(text: str) -> str:
    """Convert text to ADN representation."""
    # Convert text to bytes
    byte_array = text_to_bytes(text)
    
    # Convert bytes to ADN
    adn_str = bytes_to_adn(byte_array)
    
    return adn_str
    
    

if __name__ == "__main__":


    print(bytes_to_adn(b"Hello World!"))
    print(adn_to_bytes("TACATCTTTCGATCGATCGGACAATTTGTCGGTGACTCGATCTAACAT"))

    print(adn_to_bytes("TAATTAAT"))
    print(bytes_to_text(adn_to_bytes("TAATTAAT")))

    print(text_to_adn('''{
  "owner":"-----",
  "crypto":"NERM",
  "filename":"name.txt",  
  "data":"---"
}'''))
    
    print(adn_to_text("TGCGAACCACAAACAAACACTCGGTGTGTCGCTCTTTGACACACAGCCACACACGTACGTACGTACGTACGTACACACGAAACCACAAACAAACACTCAGTGACTGCTTGAATGTATCGGACACAGCCACACTAGCTATTTTACTAGTACACACGAAACCACAAACAAACACTCTCTCCTTCGATCTTTCGCTCATTCGTTCTTACACAGCCACACTCGCTCATTCGTTCTTACGCTGTATGCATGTAACACACGAACAAACAAAACCACAAACAAACACTCTATCATTGTATCATACACAGCCACACACGTACGTACGTACACAACCTGGT"))