# Hackathon 2025 - DNA as a Storage

A Python-based software solution for encoding, encrypting, and storing data in DNA sequences. This project integrates advanced DNA data storage techniques with AES (Advanced Encryption Standard) encryption to ensure secure and efficient file handling.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Features
- Encode data into DNA sequences for long-term storage.
- Decode DNA sequences back into their original data.
- Encrypt files using AES-256 CBC mode for secure handling.
- Decrypt files securely using the same encryption key.
- Automatically manages padding and initialization vectors (IV).
- Provides a simple and user-friendly interface.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/FyX0X/Hackaton.git
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

The project provides a command-line interface for storing and retrieving files using DNA encoding. Here's how to use it:

### First-Time Setup
1. Run the program and select 'Y' when asked if you are a new user
2. The system will generate an Owner ID and encryption key for you
3. **IMPORTANT**: Save your Owner ID and encryption key securely - you'll need them to access your files later

### Storing Files (Write Mode)
1. Run the program and select 'N' when asked if you are a new user
2. Enter your Owner ID and encryption key when prompted
3. Provide the path to the file you want to store
4. Specify the output location and filename for the DNA-encoded file
5. The system will:
   - Encrypt your file using AES-256 CBC mode
   - Convert the encrypted data into DNA sequences
   - Save the DNA sequences to the specified location
   - The file will be ready to be sent to the storage server

### Retrieving Files (Read Mode)
1. Run the program and select 'N' when asked if you are a new user
2. Enter your Owner ID and encryption key when prompted
3. Provide the file ID of the file you want to retrieve
4. Specify the output path where you want to save the decrypted file
5. The system will:
   - Retrieve the DNA sequences from the server
   - Reassemble the encrypted data
   - Decrypt the data using your key
   - Save the original file to the specified location

### Security Features
- All files are encrypted using AES-256 CBC mode before DNA encoding
- Each DNA strand includes error correction using Reed-Solomon coding
- Files are split into multiple DNA strands for efficient storage
- Each strand includes metadata (owner ID, file ID, index) and checksums
- The encryption key is never stored on the server

### Example Commands
```bash
# Write mode
python gene_vault.py --write
# Follow the prompts to enter your credentials and file details

# Read mode
python gene_vault.py --read
# Follow the prompts to enter your credentials and file details
```

### Important Notes
- Keep your Owner ID and encryption key secure - losing them means losing access to your files
- The DNA-encoded files are temporary and will be deleted after successful server storage
- The system supports any type of file (text, images, documents, etc.)
- Maximum file size depends on the server's storage capacity

## Contributing


Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

