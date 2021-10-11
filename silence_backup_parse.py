#!/usr/bin/env python3

##############################################################################
#
# Warning about extra data not stored in the SilencePlaintextBackup.xml
#
# You may want to manually press on each message and press the 🛈 button for
# each message and copy this data:
#
# - The "Sent" date on messages that are recieved from a contact
# - The timezone GMT+00:00 on both "Sent" and "Received"
# - MMS text and pictures
#   https://git.silence.dev/Silence/Silence-Android/-/issues/597
#
##############################################################################

import datetime
import re
import io
import html
import xml.etree.ElementTree as ET

phone_number = ""
input_file = "SilencePlaintextBackup.xml"
output_file = ""
your_name = ""
contacts_name = ""
write_file = True
debug = False


def fix_surrogates(s: str) -> str:
    """Inside HTML/XML, search for decimal HTML entities incorrectly encoding
    UTF-16 high/low surrogate pairs, parse the invalid entities manually,
    and encode to UTF-16 passing those surrogates so can be correctly
    interpreted on decode.

    This does not work with hexadecimal entities, and may incorrectly replace
    text in comments, etc., but is specific enough to be protected from
    false positives.
    """

    def replacement(match):
        # Parse the decimal entity to extract the Unicode points of the two
        # surrogates
        high_surrogate = int(match.group(1))
        low_surrogate = int(match.group(2))

        # Ensure those are a proper pair of high/low surrogates, not some other
        # mess. If not, return the match unchanged.
        if (0xD800 <= high_surrogate <= 0xDBFF and
           0xDC00 <= low_surrogate <= 0xDFFF):

            # Manually construct UTF-16-BE bytestring from the values of the
            # the two surrogates
            utf16_data = bytes([high_surrogate // 256, high_surrogate % 256,
                                low_surrogate // 256, low_surrogate % 256])

            # Decode the UTF-16 data thus produced, and return a valid string.
            # Since this is HTML, html.escape() just to be sure, but that
            # should not be necessary for the characters outside of BMP.
            return html.escape(utf16_data.decode('utf-16-be'))
        else:
            return match.group(0)

    # Invalid surrogate pairs look like '&#55357;&#56869;', the
    # high surrogate being in the range 55296-56319, and the low: 56320-57343.
    # Make the regex specific enough so that it does not eat anything not meant
    # for here.
    return re.sub('&#(5[56][0-9]{3});&#(5[67][0-9]{3});', replacement, s)


input_fh = open(input_file, "r")
data = (fix_surrogates(input_fh.read()))
input_fh.close()
root = ET.fromstring(data)

if write_file:
    output_fh = open(output_file, "w")
    data_to_write = ""

for sms in root.iter('sms'):
    smsType = sms.get('type')
    address = sms.get('address')

    if phone_number == address:
        epochtime = sms.get('date')
        epochtimenoms = int(epochtime[0:10])
        timestamp = datetime.datetime.fromtimestamp(epochtimenoms)
        timestamp_readable = timestamp.strftime('%Y-%m-%d %H:%M:%S')

        if debug:
            if smsType == "2":
                print("SMS from", your_name, "to", contacts_name)
            elif smsType == "1":
                print("SMS from", contacts_name, "to", your_name)

            print("Sent:     ", timestamp_readable)
            if smsType == "1":
                print("Received: ", timestamp_readable)
            print("\n" + sms.get("body"), "\n")
            print("=" * 40)

        if write_file:
            if smsType == "2":
                data_to_write += ("SMS from " +
                                  your_name + " to " + contacts_name + "\n")
            elif smsType == "1":
                data_to_write += ("SMS from " +
                                  contacts_name + " to " + your_name + "\n")

            data_to_write += "Sent:     " + timestamp_readable + "\n"
            if smsType == "1":
                data_to_write += "Received: " + timestamp_readable + "\n"

            data_to_write += "\n" + sms.get("body") + "\n"
            data_to_write += "\n" + "=" * 40 + "\n"

if write_file:
    output_fh.write(data_to_write)
    output_fh.close()
