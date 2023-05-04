# Hive Heating Online Checker

> TODO: Full documentation.

## Introduction

These scripts are to enable the polling of a Hive Heating system, to check it is online - they were written, because my boiler circuit breaker is sensitive and sometimes trips taking the heating offline (which is _really_ annoying in winter!)

Whichever device will be running the scripts needs a registering with the Hive API (including 2FA, if configured). This is achieved with the `registerDevice.py` script.
Ensure that `app.ini` is setup, before running.

You should also run the `gmailSender.py` script once, to go through the GMail setup. See the top of the script for the oAuth setup you will need to do, to create and authorise the application access.
Ensure that `mail.ini` is setup before running.

The `checkHiveOnline.py` script can then be used (via a _cronjob_ or similar) to poll.
Ensure that `webhook.ini` is setup before running.