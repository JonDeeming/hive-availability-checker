from os.path import exists
from configparser import ConfigParser
from getpass import getpass
from pyhiveapi import Hive, SMS_REQUIRED

def main():
    if exists('app.ini'):
        print('Found an existing "app.ini" file. Cannot continue.')
        exit(1)

    config = ConfigParser()
    config.read('app.ini')

    username = input('Enter Hive Username: ')
    password = getpass(prompt = 'Enter Hive Password: ')

    session = Hive(
        username=username,
        password=password,
    )
    try:
        login = session.login()
    except TypeError:
        exit(1)

    if login.get("ChallengeName") == SMS_REQUIRED:
        code = input("Enter 2FA code: ")
        try:
            session.sms2fa(code, login)
        except TypeError:
            exit(1)

    session.auth.device_registration('HiveOnlineChecker')
    deviceData = session.auth.get_device_data()

    config.add_section('Hive Login')
    config.set('Hive Login','username',username)
    config.set('Hive Login','password',password)

    config.add_section('Device Keys')
    config.set('Device Keys','group_key',deviceData[0])
    config.set('Device Keys','device_key',deviceData[1])
    config.set('Device Keys','device_password',deviceData[2])

    with open('app.ini', 'w' ) as file:
        config.write(file)


if __name__ == '__main__':
    main()