def write(filename: str, crypto_method: str, data: str) -> str:
    output = ""
    output += "AAAA"


def text_to_bytes(text: str) -> bytes:

    binary = bytes(text, "utf-8")
    return binary


def bytes_to_base_4(input_byte: bytes) -> str:
    binary_str = ''.join(format(byte, '08b') for byte in input_byte)
    if len(binary_str) % 2 != 0:
        binary_str = '0' + binary_str


print(text_to_binary("hello"))
