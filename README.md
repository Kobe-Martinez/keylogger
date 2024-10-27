# Keylogger Project


## Overview


This Keylogger project captures keystrokes, clipboard data, system information, screenshots, and audio recordings on a Windows machine. It encrypts the collected data and sends it via email using the Gmail API. Once the encrypted emails have been received, the user must download them into the main file path and run the decryption file to retrieve the data. 

This project serves educational purposes only and should not be used for malicious activities.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Set up Gmail API](#set-up-gmail-api)
- [Usage](#usage)
- [Features](#features)
- [Email Configuration](#email-configuration)
- [Encryption Details](#encryption-details)
- [Decryption Details](#decryption-details)
- [Contributing](#contributing)
- [License](#license)
- [Important Note](#important-note)


## Prerequisites

```bash
- Python 3.12.5 or higher
- Required libraries (see below for installation)
- Gmail account for email functionality
```

## Project Structure

The primary files in this project include:

```bash
1. Keylogger.py: Main script to capture keystrokes, screenshots, system information, clipboard data, and microphone recordings.

2. encryption_util.py: Contains utilities to generate an encryption key and encrypt files.

3. decryption_util.py: Provides a method to decrypt the encrypted files.

4. credentials.json: Contains client information required for Gmail OAuth 2.0 authentication. Obtained from Google Cloud Console.

5. token.json: Stores access and refresh tokens after Gmail authentication. File is obtained from running the main script "Keylogger.py"
```

## Installation

1. **Clone the repository:**
   Open your terminal or command prompt and run:

	```bash
	git clone https://github.com/Kobe-Martinez/Keylogger.git
	cd Keylogger
	```


2. **Install required libraries:** 
   You can install all required libraries by downloading the requirements.txt file and running:

	```bash
	pip install -r requirements.txt
	```

## Set Up Gmail API

Step 1: Set Up Gmail API on Google Cloud Console


- Open Google Cloud Console and create a new project or select an existing one.

- Enable the Gmail API:
	- Go to the API & Services Dashboard.
	- Search for and enable the Gmail API.
- Create OAuth 2.0 Credentials:
	- In the Credentials tab, click on Create Credentials and select OAuth Client ID.
	- When prompted, select Desktop App as the application type.
	- Download the JSON credentials file:
		- After creation, download this file, naming it credentials.json.
		- Save this file in the same directory as your Python script.


Step 2: Set Up OAuth Consent Screen

- Go to OAuth Consent Screen:
	- Under User Type, select External (if you plan to use this beyond your Google 	account, otherwise Internal is fine).
- Fill Out the Consent Screen Information:
	- App Name: Enter a name for your app (e.g., “Keylogger App”).
	- User Support Email: Enter your email.
	- Developer Contact Information: Enter your email here as well (can be the same as 	your User Support Email).
- Click Save and Continue to finish setting up the consent screen.


Step 3: Configure OAuth Scopes

- Skip adding additional scopes here, as the Gmail scope (https://www.googleapis.com/auth/gmail.send) will be specified directly in your Python code.
- Click Save and Continue.


Step 4: Finish Setup

- Click Done in the Google Cloud Console.
- Your app is now set up to use the Gmail API securely through OAuth 2.0, allowing it to send emails from Gmail.


Step 5: Add Test Users

Since your app is unverified, Google only allows access to users you explicitly list as test users in the Google Cloud project. Here's how you can add yourself or others as test users:

- Go to Google Cloud Console.
- Select your project: Choose the project associated with your keylogger app.
- Go to OAuth consent screen:
	- On the left-hand menu, select APIs & Services > OAuth consent screen.
- Add Test Users:
	- Under Test users, add the email addresses (including your own) of people who will 	access the app.
- Save Changes.

This will allow only the listed users to bypass the "App not verified" screen and use the app.


## Usage

1. Modify Paths: Before running the script, modify the file paths in ``` Keylogger.py and decryption_util.py ``` according to your system's directory structure. Update the file_path variable to point to your project folder.

2. Configure Email Settings: Edit the Keylogger.py file and set the following variables:

```bash
   email_address = "your_email@gmail.com"  # Your Gmail address
   toaddr = "recipient_email@gmail.com"     # Recipient's email address
```

3. Run the Keylogger: Execute the Keylogger script using:

   ```bash
   python Keylogger.py
   ```

   The script will start running and log keystrokes, clipboard data, system information, audio recordings, and screenshots. 

To stop the logging process, press the ``` Esc key ```. This will trigger the encryption and email-sending processes.

4. Download the Encrypted Files: Once the encrypted files have been sent to the desired email, download them to the main file path ensuring that it is in the same folder as Keylogger.py

5. Modify the Decryption List and Run the Decryption file: To decrypt these files, you must modify the ```bash files_to_decrypt ```  list in ```bash decryption_util.py ```. Put all the encrypted files in this list, then execute the script using: 

```bash
python decryption_util.py
```

Once the script is finished executing, open the encrypted files (the files that were just downloaded and are now decrypted) and you will be able to see the decrypted data. 

## Features

- Keystroke Logging: Captures all keystrokes typed on the keyboard.

- Clipboard Monitoring: Records any text copied to the clipboard.

- System Information Logging: Gathers system details like hostname, processor, operating system, and IP addresses.

- Audio Recording: Records audio from the microphone for a specified duration.

- Screenshot Capture: Takes a screenshot of the screen.

- File Encryption: Encrypts the collected logs before sending them.

- Email Delivery: Sends the logs to a specified email address using the Gmail API.

- File Decryption: Decrypts the collected logs after receiving them through email.

## Email Configuration

- OAuth 2.0 Authentication: When you run the script for the first time, it will open a browser window for you to authenticate your Gmail account. Follow the prompts to grant access.

- Token Storage: After authentication, the access and refresh tokens will be stored in token.json, allowing future logins without re-authentication.


## Encryption Details

- generate_key: Creates or loads an encryption key in encryption_key.key.

- encrypt_file: Encrypts a file using the Fernet symmetric encryption.

## Decryption Details

- decrypt_file: Decrypts an encrypted file. 

- Uses generate_key from encryption_util.py to retrieve the encryption key. 

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Important Note

This Keylogger is intended for educational purposes only. Ensure that you have permission to monitor any system and comply with local laws and regulations regarding privacy and data collection. Misuse of this program can lead to severe consequences.
