# Importing Fernet for encryption
from cryptography.fernet import Fernet

# Importing os for file path operations
import os

# Function to generate and save an encryption key:
def generate_key(key_file_path):
    # Check if the key file already exists
    if not os.path.exists(key_file_path):
        # Generate a key only if it doesn't already exist
        # new encryption key
        key = Fernet.generate_key()
        # Save the key in a secure place for future decryption
        #  Open the file in binary write mode
        with open(key_file_path, "wb") as key_file:
            # Write the key to the file
            key_file.write(key)
    else:
        # Load the existing key
        # Open the file in binary read mode
        with open(key_file_path, "rb") as key_file:
            # Read the existing key
            key = key_file.read()
    # Return the generated or loaded key
    return key

# function to encrypt a file:
def encrypt_file(file_path, key):
    # Create a Fernet object with the provided key
    lock = Fernet(key)
    # Open the file in binary read mode
    with open(file_path, "rb") as file:
        # Read the original data from the file
        original_data = file.read()
    # Encrypt the data
    encrypted_data = lock.encrypt(original_data)
    # Open the file in binary write mode to overwrite
    with open(file_path, "wb") as encrypted_file:
        # Write the encrypted data back to the file
        encrypted_file.write(encrypted_data)