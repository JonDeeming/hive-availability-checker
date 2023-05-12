import logging
import gmailSender

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s : %(message)s')
    logging.info('Authenticating with Google.')
    creds = gmailSender.auth()

if __name__ == '__main__':
    main()