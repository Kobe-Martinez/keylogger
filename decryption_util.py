# Importing Fernet for decryption
from cryptography.fernet import Fernet

# Importing the function to generate/load encryption key
from encryption_util import generate_key


# Function for decrypting files
def decrypt_file(file_path, key):
    # Create a Fernet object with the provided key
    unlock = Fernet(key)
    # Open the encrypted file in binary read mode
    with open(file_path, "rb") as encrypted_file:
        # Read the encrypted data from the file
        encrypted_data = encrypted_file.read()
        # Decrypt the data
    decrypted_data = unlock.decrypt(encrypted_data)
    # Open the file in binary write mode to overwrite
    with open(file_path, "wb") as decrypted_file:
        # Write the decrypted data back to the file
        decrypted_file.write(decrypted_data)

# Path to the key file
key_file_path = "encryption_key.key"

# Generate or load the encryption key
key = generate_key(key_file_path)

# Base file path
file_path = "C:\\Users\\Kobe\\Desktop\\Resume_Project\\projKeylogger_1\\Project"

# File path extension for Windows
extend = "\\"

# Complete file path
file_merge = file_path + extend

# List of files to decrypt
files_to_decrypt = ["test_audio.wav", "test_clipboard.txt", "test_key_log.txt", "test_screenshot.png", "test_systeminfo.txt"]

# Loop through each file and decrypt it
for file in files_to_decrypt:
    # Decrypt each file using the key
    decrypt_file(file_merge + file, key)


