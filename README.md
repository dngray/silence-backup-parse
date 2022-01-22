# Silence backup parse

I wanted to export my [Silence](https://silence.im) messages as I'm going to stop using the app. Most of my contacts had moved to more secure messengers such as [Signal](https://signal.org) or [Matrix](https://matrix.org) anyway.

There are unpatched vulnerabilities with some of the libraries [Silence](https://silence.im), uses. The software does largely [seem unmaintained](https://git.silence.dev/Silence/Silence-Android/-/commits/master/).

Additionally SMS metadata cannot be secured, and SMS/MMS should be avoided in general.

This script will read in your `SilencePlaintextBackup.xml` and export the SMS messages out into a readable format which you then may store somewhere secure such as:

```
========================================
SMS from <you> to <recipient>
Sent:     YYYY-MM-DD 00:00:00

message

========================================
```

## What isn't exported

It should be noted however certain data does not exist in the `SilencePlaintextBackup.xml` export format such as:

- The "Sent" date on messages that are recieved from a contact
- The timezone GMT+00:00 on both "Sent" and "Received"
- MMS text and pictures [issue #597](https://git.silence.dev/Silence/Silence-Android/-/issues/597)

## Alternatives

I'd recommend if you must use SMS, switching to one of these alternatives:

- AOSP Messenger app with [SMS Import / Export](https://f-droid.org/en/packages/com.github.tmo1.sms_ie/)

Or a Matrix bridge (if you run your own Matrix server):

- [Android SMS](https://gitlab.com/beeper/android-sms)
