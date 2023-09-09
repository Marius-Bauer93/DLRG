""" Script to deliver information via email

This script 'mail_service.py' provides an automation to send
several templated HTML emails to multiple different recipients.

Example call:
    Please refer to README.md

To-Do:
    - integrate file path option to argparse
    - integrate subject to argparse
    - make reciever become a list and loop over participants
    - add "sewobe" REST API user collection service

DLRG mail config details:
    https://atlas.dlrg.de/confluence/display/AN/E-Mail

This script was created by: unbelievablebauer@t-online.de
The last update of the content happend at: 09.09.2023
"""

# Libaries
# System
import os
# Input
import argparse
import getpass
# Email
import smtplib
import ssl
from email.mime.text import MIMEText as format
from email.mime.multipart import MIMEMultipart as render

class email:
    """Provides email communication environment."""

    def __init__(self, sender: str, reciever: str, mail_system: str, mail_port: int, mail_user: str, password: str, debug: bool) -> None:
        """Initialize required mail authentication details.

        This method prepares a vaild mail connection to send out
        mails via DLRG mail systems.
        Args:
            sender      (str): shown mail address in sender section
            reciever    (str): mail address which recieves the mail
            mail_system (str): mail server handling the SMTP request
            mail_port   (int): SMTP port of the mail server
            mail_user   (str): user account registered to the mail server
            password    (str): password for the registered user account
            debug      (bool): global variable for verbose output
        
        Returns:
            None
        
        """
        # Variables of the entire class
        # Participants
        self.sender_email = sender
        self.reciever_email = reciever
        # Mail environment
        self.mail_server = mail_system
        self.mail_server_port = mail_port
        self.mail_account = mail_user
        self.password = password
        # Output
        self.debug = debug

        # Mail direction information
        if self.debug:
            print("Email environment successfully provided:\n")
            print(f"FROM: {self.sender_email}\nTO: {self.reciever_email}\n")
            print(f"Mail system: {self.mail_server}\nMail port: {self.mail_server_port}\nUser: {self.mail_account}")

    def load_mail_body(self, file_location: str) -> str:
        """Reads the selected HTML template content.

        This modules loads the selected HTML body template, which
        should be selected as email body.
        Args:
            file_location (str): predefined file location combined with HTML template name
        
        Returns:
            Str: read HTML content
        
        """
        # Load selected HTML body template
        with open(file_location, "r") as mail_body:
            html_message = mail_body.read()

        return html_message
    
    def render_mail(self, subject: str, content: str) -> str:
        """Rendering of the entire email.

        This method renderes the given information snippets into a
        valid email layout, which can be forwarded to a mail system.
        Args:
            subject (str): contains the subject of the email 
            content (str): contains the entire mail body layout
        
        Returns:
            Str: The entire email mapped into a single string
        
        """
        # Prepare email framework
        mail_meassage = render("alternative")
        mail_meassage["Subject"] = subject
        mail_meassage["From"] = self.sender_email
        mail_meassage["To"] = self.reciever_email

        # # Format HTML objects with MIMEtext
        mail_body = format(content, "html")

        # Renders formated HTML body with MIMEMultipart into a full email
        mail_meassage.attach(mail_body)

        # Mail body layout
        if self.debug:
            print(f"\nMail body:\n{mail_meassage.as_string()}\n")

        return mail_meassage.as_string()

    def send_secure_mail(self, message: str) -> None:
        """Sends an encrypted email.

        This module takes care of encrypting the rendered email and forwarding
        the email to the mail delivery system, so that the mail can be sent.
        Args:
            message (str): contains the entiere mail framework with content
        
        Returns:
            None
        
        """
        # Create secure connection
        connection = ssl.create_default_context()
        
        #Prepare SMTP communication
        with smtplib.SMTP_SSL(self.mail_server, self.mail_server_port, context=connection) as mail_server:
            # Mail server authentication
            session = mail_server.login(self.mail_account, self.password)
            if self.debug:
                print(f"Login attempt: {session}\n")

            # Send mail
            delivery_status = mail_server.sendmail(self.sender_email, self.reciever_email, message)
            if self.debug:
                if len(delivery_status) == 0:
                    print(f"Mail shipping status: Delivered successfully!\n")
                else:
                    print(f"Mail shipping status: {delivery_status}\n")

if __name__ == '__main__':
    # Prepares container to collect CLI input
    PARSER = argparse.ArgumentParser(description="Load relevant mail environment information.")

    # Add the expected input parameters
    PARSER.add_argument("-s", "--sender", required=True, type=str, dest="sender", help="From where the mail is sent.")
    PARSER.add_argument("-r", "--reciever", nargs="*", required=True, type=str, dest="reciever", help="List of persons who should recieve the mail.")
    PARSER.add_argument("-ms", "--mail-server", required=False, type=str, dest="mail_server", default="mail.dlrg.de", help="FQDN from involved mail delivery system.")
    PARSER.add_argument("-mp", "--mail-port", required=False, type=int, dest="mail_port", default=465, help="SMTP port from the mail delivery system.")
    PARSER.add_argument("-u", "--user", required=True, type=str, dest="user", help="Registered mail user account for authentication.")
    PARSER.add_argument("-p", "--password", required=False, type=str, dest="password", default="123", help="Password from mail user.")
    PARSER.add_argument("-v", "--verbose", required=False, type=bool, dest="debug", default=False, help="Bool to provide verbose output.")
    
    # Load gathered inputs
    ARGS = PARSER.parse_args()

    # Collect real password via CLI
    if ARGS.password == "123":
        ARGS.password = getpass.getpass("Please enter your password:")

    # Rerender ARGS values, if type matches a list
    # TO-DO
    if type(ARGS.reciever) == list:
        ARGS.reciever = ARGS.reciever[0]

    # Check input
    if ARGS.debug:
        print(f"Authentication data: {ARGS.sender}, {ARGS.reciever}, {ARGS.mail_server}, {ARGS.mail_port}, {ARGS.user}, {ARGS.debug}\n")

    # HTML folder location
    DIR_PATH = f"{os.path.dirname(os.path.realpath(__file__))}/templates/html_mail_body/"

    # Initialize mail service
    MY_MAIL = email(ARGS.sender, ARGS.reciever, ARGS.mail_server, ARGS.mail_port, ARGS.user, ARGS.password, ARGS.debug)

    # Mail delivery service call
    # TO-DO
    MY_MAIL.send_secure_mail(MY_MAIL.render_mail("DRYrun", MY_MAIL.load_mail_body(f"{DIR_PATH}test.html")))