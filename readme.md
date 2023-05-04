# Hive Heating Online Checker

> TODO: Full documentation.

## Introduction

These scripts are to enable the polling of a Hive Heating system, to check it is online - they were written, because my boiler circuit breaker is sensitive and sometimes trips taking the heating offline (which is _really_ annoying in winter!)

Whichever device will be running the scripts needs a registering with the Hive API (including 2FA, if configured). This is achieved with the `registerDevice.py` script.
Ensure that `app.ini` **does not exist**, before running - as the script creates it.

You should also run the `gmailSender.py` script once, to go through the GMail setup. See the top of the script for the oAuth setup you will need to do, to create and authorise the application access.
Ensure that `mail.ini` is setup before running.
If you are setting this up on a remote device, you will need to have a remote session that supports creating a browser (such as RDP or VNC), due to Google's desktop authentication flow.

The `checkHiveOnline.py` script can then be used (via a _cronjob_ or similar) to poll.
Ensure that `webhook.ini` is setup before running.

> Note: Ensure you restrict permissions to the `*.ini` files, as they will contain keys and credentials. **Do not commit them to git!**

## Latency

Be aware that the Hive API will report healthy status even if items show offline in their app - sometimes for several minutes.

It is not unusual for a latency of 10 minutes from the system losing power, to the API reporting that.
