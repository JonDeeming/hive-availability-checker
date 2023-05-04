import logging
import os
import requests
from configparser import ConfigParser
from pyhiveapi import Hive
import gmailSender
DEVICE_REQUIRED = "DEVICE_SRP_AUTH" # Not exposed as a separate const in the library (yet?)

def init():
    if os.environ.get('LOGLEVEL') != None:
        logging.basicConfig(level=os.environ.get('LOGLEVEL').upper(), format='%(asctime)s - %(levelname)s : %(message)s')
        logging.debug('EnvVar "LOGLEVEL" found, setting logging to ' + os.environ.get('LOGLEVEL').upper())
    else:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')

    if os.environ.get('SEND_ON_OK') != None:
        if os.environ.get('SEND_ON_OK').upper() == 'TRUE':
            logging.debug('EnvVar "SEND_ON_OK = TRUE" found - will send notifications for all events.')
            return True
        else:
            logging.debug('EnvVar "SEND_ON_OK" not found, or not "TRUE" - will send notifications for unaccessible events only.')
            return False # Set as False to only send mails when Hive is unreachable.
    
    return False

def notifyMail(message):
    logging.debug('Loading and parsing "mail.ini" file.')
    mailConfig = ConfigParser()
    mailConfigFile = r'./mail.ini'
    mailConfig.read(mailConfigFile)

    to_address = mailConfig.get('GMail', 'to_smtp')
    from_address = mailConfig.get('GMail', 'from_smtp')
    subject_text = mailConfig.get('GMail', 'subject_text')

    creds = gmailSender.auth()
    gmailSender.send_mail(creds, to_address, from_address, subject_text, message)

def notifyWebhook(healthy):
    logging.debug('Loading and parsing "webhook.ini" file.')
    webhookConfig = ConfigParser()
    webhookConfigFile = r'./webhook.ini'
    webhookConfig.read(webhookConfigFile)

    healthy_webhook = webhookConfig.get('Webhook', 'healthy')
    unhealthy_webhook = webhookConfig.get('Webhook', 'unhealthy')

    if healthy == True:
        logging.info('Calling healthy webhook.')
        response = requests.post(healthy_webhook, headers={'Content-Type':'application/json'})
        logging.info('Webhook status code: ' + str(response.status_code))
    else:
        logging.info('Calling unhealthy webhook')
        response = requests.post(unhealthy_webhook, headers={'Content-Type':'application/json'})
        logging.info('Webhook status code: ' + str(response.status_code))

def main():
    SEND_ON_OK = init()

    logging.debug('Loading and parsing "app.ini" file.')
    config = ConfigParser()
    configFile = r'./app.ini'
    config.read(configFile)

    username = config.get('Hive Login', 'username')
    password = config.get('Hive Login', 'password')
    logging.info("Hive login: " + username)

    # Create session
    session = Hive(
        username=username,
        password=password,
    )
    # Add device keys to the auth object:
    session.auth.device_group_key = config.get('Device Keys', 'group_key')
    session.auth.device_key = config.get('Device Keys', 'device_key')
    session.auth.device_password = config.get('Device Keys', 'device_password')

    # Login using device credentials.
    logging.debug('Authenticating with Hive.')
    login = session.login()
    if login.get("ChallengeName") == DEVICE_REQUIRED:
        session.deviceLogin()
    else:
        logging.error('Login failed - Confirm this device is registered.')
        exit(1)

    # Create a session, now that we're authenticated and authorized.
    logging.debug('Starting Hive session - querying devices.')
    session.startSession()

    logging.debug("Climate Device Online: " + str(session.deviceList['climate'][0]['deviceData']['online']))
    if session.deviceList['climate'][0]['deviceData']['online'] == True:
        logging.info('Hive climate is online.')
        if SEND_ON_OK:
            logging.debug('Sending mail notification for online status.')
            notifyMail('Hive climate system is accessible')
        logging.debug('Sending webhook healthy call.')
        notifyWebhook(True)
    else:
        logging.info('Hive climate is offline.')
        logging.debug('Sending mail notification for offline status.')
        notifyMail('Hive climate system is unavailable. Check the boiler circuit breaker.')
        logging.debug('Sending webhook unhealthy call.')
        notifyWebhook(False)


if __name__ == '__main__':
    main()