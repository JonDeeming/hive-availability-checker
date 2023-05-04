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

It is not unusual for a latency of 10 minutes from the system losing power, to the API reporting an unhealthy status.

Power resumption is generally quicker to report, within 1-2 minutes under normal circumstances.

## Why Not _Home Assistant_?

My first thought was to use _Home Assistant_, but (unless I _totally_ missed something) whilst it can see the Hive thermostat move to an `Unavailable` state, the _Home Assistant_ integration does not support triggering a rule on that event. It can only trigger upon _"On"_ and _"Off"_ style status, not when no status is available (it just leaves the device on the prior polled status.)

Luckily, the Home Assistant [Hive Integration](https://github.com/Pyhass/Pyhiveapi) can be used in a stand-alone Python application - so I used that to login and parse the _JSON_ from the API (hacky... but it works).

From there I use a local webhook on my _Hubitat_ system to toggle a virtual lock, which is offered to Amazon Alexa and an _Alexa Routine_ will trigger and give me a voice alert.

And I can get mails, from GMail, in the event that the webhook/alert were to fail.

It would have been nice to do this in _Home Assistant_, but I couldn't find a way to make it work.
