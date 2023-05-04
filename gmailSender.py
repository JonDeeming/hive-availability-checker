# See this article on creation of GMail oAuth credentials...
# https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application
# Ensure that the Google App that you are publishing has the GMail API enabled.
# Make sure to include the correct scope (/auth/gmail.modify).

from __future__ import print_function
import os.path
import base64
import logging
from email.message import EmailMessage
from configparser import ConfigParser

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.debug('Authenticating with Google.')
    creds = auth()

    logging.debug('Loading and parsing "mail.ini" file.')
    config = ConfigParser()
    configFile = r'./mail.ini'
    config.read(configFile)

    to_address = config.get('GMail', 'to_smtp')
    from_address = config.get('GMail', 'from_smtp')

    logging.info('Sending test message from ' + from_address + ' going to ' + to_address + ".")
    send_mail(creds, to_address, from_address, 'Test Message Subject', 'Test Message Body')

def auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        logging.debug('Loading Google credentials from "token.json".')
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logging.debug('Attempting to refresh Google Token.')
            creds.refresh(Request())
        else:
            logging.debug('No token found, starting login process.')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            logging.debug('Token cached in "token.json"')

    return creds

def send_mail(creds, to_smtp, from_smtp, subject_text, message_text):
    try:
        # create gmail api client
        logging.debug('Building GMail message.')
        service = build('gmail', 'v1', credentials=creds)
        message = EmailMessage()

        message.set_content(str(message_text))

        message['To'] = str(to_smtp)
        message['From'] = str(from_smtp)
        message['Subject'] = str(subject_text)

        # encoded message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {
                'raw': encoded_message
        }
        logging.debug('Sending mail from ' + from_smtp + ' to ' + to_smtp + '.')
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId="me", body=create_message).execute())

        logging.info(F'Message Id: {send_message["id"]}')

    except HttpError as error:
        logging.error(F'An error occurred: {error}')
        send_message = None

    return send_message


if __name__ == '__main__':
    main()