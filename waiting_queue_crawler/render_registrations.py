""" Script to crawl mails and render them into json format

This script 'render_registrations.py' provides an automation to crawl
mails with IMAP protocol so that their content can be processed in json
format for different usecases.

Example call:
    Please refer to README.md

To-Do:
    - #

DLRG mail config details:
    https://atlas.dlrg.de/confluence/display/AN/E-Mail

This script was created by: unbelievablebauer@t-online.de
The last update of the content happend at: 01.03.2024
"""

# Libaries
# System
import os
# Input
import argparse
import getpass
# Data
import json
# Email
import imaplib
import email
from email.header import decode_header
from email.utils import parseaddr

class imap_session:
    """Provides a secure connection with the IMA Protocol to extract mail raw data."""

    def __init__(self) -> None:
        """Initialize empty IMA Protocol session.

        #
        Returns:
            None
        """
        pass
        
    def decode_subject(encoded_subject: str) -> list:
        """Function to decode email subject.

        #
        Args:
            encoded_subject (str): Decoded mail object

        Returns:
            list: The decoded email content
        """
        decoded_parts = decode_header(encoded_subject)
        decoded_subject = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                decoded_subject.append(part.decode(encoding or 'utf-8'))
            elif isinstance(part, str):
                decoded_subject.append(part)
        return ''.join(decoded_subject)

    def parse_string_to_dict(input_string: str) -> dict:
        """Function to rerender sting into a dictionary.

        #
        Args:
            input_string (str): Single sting to become rendered

        Returns:
            dict: Iteratable data to be processed for upload
        """
        # Split the string into lines
        lines = input_string.split('\r\n')
        
        # Initialize an empty dictionary
        result_dict = {}
        
        # Iterate over each line
        for line in lines:
            # Split each line at the first occurrence of ":"
            key_value_pair = line.split(':', 1)
            
            # Check if the line contains a key-value pair
            if len(key_value_pair) == 2:
                # Remove leading/trailing whitespace from the key
                key = key_value_pair[0].strip()
                # Remove leading/trailing whitespace from the value
                value = key_value_pair[1].strip()
                result_dict[key] = value
        
        return result_dict

    def save_email_as_json(email_message: str, output_folder: str) -> None:
        """Function to save email as .json file.

        #
        Args:
            email_message (str): Content of the decoded email
            output_folder (str): Path where to store all crawled objects to
        Returns:
            None
        """
        email_data = {
            "From": parseaddr(email_message.get("From"))[1],
            "To": parseaddr(email_message.get("To"))[1],
            "Subject": imap_session.decode_subject(email_message.get("Subject")),
            "Date": email_message.get("Date"),
            "Body": "",
        }
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                # merge to single sting
                email_data["Body"] += part.get_payload(decode=True).decode(part.get_content_charset())
                # replace sting against rendered dictionary
                email_data["Body"] = imap_session.parse_string_to_dict(email_data["Body"])
        # Generate unique filename
        filename = os.path.join(output_folder, f"{email_message['Message-ID'].strip('<').strip('>').strip('@dlrg.de')}.json")
        with open(filename, "w+") as json_file:
            json.dump(email_data, json_file, indent=4)

if __name__ == '__main__':
    # Prepares container to collect CLI input
    PARSER = argparse.ArgumentParser(description="Load relevant mail environment information.")

    # Add the expected input parameters
    PARSER.add_argument("-ms", "--mail-server", required=False, type=str, dest="mail_server", default="mail.dlrg.de", help="FQDN from involved mail delivery system.")
    PARSER.add_argument("-mp", "--mail-port", required=False, type=int, dest="mail_port", default=993, help="IMAPS port from the mail delivery system.")
    PARSER.add_argument("-u", "--user", required=True, type=str, dest="user", help="Registered mail user account for authentication.")
    PARSER.add_argument("-p", "--password", required=False, type=str, dest="password", default="123", help="Password from mail user.")
    PARSER.add_argument("-f", "--folderpath", required=False, type=str, dest="folderpath", default="Online-Anmeldungen/unbearbeitet", help="Mailbox folder location to crawl mails from.")
    PARSER.add_argument("-v", "--verbose", required=False, type=bool, dest="debug", default=False, help="Bool to provide verbose output.")
    
    # Load gathered inputs
    ARGS = PARSER.parse_args()

    # Collect real password via CLI
    if ARGS.password == "123":
        ARGS.password = getpass.getpass("Please enter your password:")

    # Connect to IMAP server and login
    mail = imaplib.IMAP4_SSL(ARGS.mail_server, ARGS.mail_port)
    login_result, login_message = mail.login(ARGS.user, ARGS.password)

    # Folder to read emails from
    FOLDER_NAME = f"INBOX/{ARGS.folderpath}"

    # Check the response from the server
    if ARGS.debug:
        if login_result == 'OK':
            print("Login successful!")
        else:
            print("Login failed:", login_message)

        # Get a list of selectable folders
        selectable_folders = mail.list()

        # Print the selectable folders
        for folder in selectable_folders[1]:
            print(folder)

    # Select the folder to read emails from
    mail.select(FOLDER_NAME)

    # rendered mail folder location
    DIR_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/registration_mails"

    # Search for all emails in the selected folder
    result, data = mail.search(None, "ALL")

    if result == "OK":
        for num in data[0].split():
            result, message_data = mail.fetch(num, "(RFC822)")
            if result == "OK":
                email_message = email.message_from_bytes(message_data[0][1])
                # Save the email as .json file
                imap_session.save_email_as_json(email_message, DIR_PATH)
                print("Email saved as .json file:", email_message.get("Message-ID").strip('<').strip('>').strip('@dlrg.de'))
    else:
        print("Failed to search emails.")

    # Close connection
    mail.close()
    mail.logout()
