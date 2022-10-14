# bdmaker

A simple script to annotate a contact in my google addressbook with a birthday.

## Setup

1. [Enable the goolge API](https://console.cloud.google.com/flows/enableapi?apiid=people.googleapis.com)
2. [Authorice the credentials](https://developers.google.com/people/quickstart/python#authorize_credentials_for_a_desktop_application) and save the json as `credentials.json` in this folder.
3. Install the dependencies with `pip install -r requirements.txt`

## Usage

```
python3 bdmaker.py "Alan Turing: 1954-06-07"
```

The name of the person doesn't have to exactly match the contact because the
script uses google's search feature and will match any similar named contacts.

Moreover the date can be in the following formats:

- yyyy-mm-dd (eg: 2000-11-23)
- dd.mm.yyyy (eg: 23.11.2000)
- dd.mm (eg: 23.11) for when you only know the birthday but not the year
