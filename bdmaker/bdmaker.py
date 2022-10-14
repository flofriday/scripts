import argparse
from dataclasses import dataclass

import os.path
import re
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


@dataclass
class Date:
    """
    A custom date implementation because sometimes we only know the birthday
    but not the year.
    """

    day: int
    month: int
    year: int

    def __repr__(self):
        out = f"{self.day:02d}.{self.month:02d}"
        if self.year is not None:
            out += f".{self.year}"
        return out


@dataclass
class Person:
    name: str
    birthdate: Date
    google_id: str
    google_etag: str


def parse_input(input):
    (name, datetext) = input.split(":")
    name = name.strip()
    datetext = datetext.strip()

    # Parse european date format dd.mm.yyy (eg: 23.11.2000)
    # Note the year is optional here.
    if re.match(r"\d{2}\.\d{2}(\.\d{4})?", datetext):
        (day, month, _, year) = re.search(
            r"(\d{2})\.(\d{2})(\.(\d{4}))?", datetext
        ).groups()
        date = Date(day, month, year)

    # Parse ISO format yyyy-mm-dd (eg: 2000-11-23)
    elif re.match(r"(\d{4})-(\d{2})-(\d{2})", datetext):
        (year, month, day) = re.match(r"(\d{4})-(\d{2})-(\d{2})", datetext).groups()
        date = Date(int(day), int(month), int(year))

    # Date parsing error
    else:
        print(
            "ERROR: I cannot parse the date.\nI can only read dates in the european or ISO format.",
            file=sys.stderr,
        )
        exit(1)

    return Person(name, date, None, None)


def google_auth():
    # If modifying these scopes, delete the file token.json.
    SCOPES = ["https://www.googleapis.com/auth/contacts"]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def parse_google_person(p):
    google_id = p["resourceName"]
    google_etag = p["etag"]
    name = p["names"][0]["displayName"]
    date = None

    try:
        dateinfo = p["birthdays"][0]["date"]
        day = dateinfo["day"]
        month = dateinfo["month"]
        date = Date(day, month, None)
        year = dateinfo["year"]
        date = Date(day, month, year)
    except KeyError:
        pass

    return Person(name, date, google_id, google_etag)


def find_person(service, target):
    req = service.people().searchContacts(
        query=target.name, readMask="names,birthdays", pageSize=64
    )
    results = req.execute()

    try:
        persons = list(
            map(lambda r: parse_google_person(r["person"]), results["results"])
        )
    except KeyError:
        persons = []

    if len(persons) == 0:
        print("The name didn't match anyone in your contacts.")
        exit(0)

    elif len(persons) == 1:
        person = persons[0]
        # If the name is not the same ask if it is the correct person
        if target.name.lower() != person.name.lower():
            print("Is this the person you meant? (Y/n)")
            print(f"{person.name}: {person.birthdate}")
            answer = input("> ")
            if answer.lower() != "y":
                exit(0)
        elif person.birthdate is not None:
            print(
                "The person already has a birthday, do you want to override it? (Y/n)"
            )
            print(f"{person.name}: {person.birthdate}")
            answer = input("> ")
            if answer.lower() != "y":
                exit(0)

        # If the person already has a birthday ask if it should be overwritten
        return person

    else:
        print("Which of them should be updated:")
        for (n, person) in enumerate(persons):
            print(f"[{n}] {person.name}: {person.birthdate}")
        selection = int(input("> "))
        return persons[selection]


def update_person(service, person: Person):
    body = {
        "etag": person.google_etag,
        "birthdays": [
            {
                "date": {
                    "day": person.birthdate.day,
                    "month": person.birthdate.month,
                    "year": person.birthdate.year,
                },
            },
        ],
    }

    try:
        result = (
            service.people()
            .updateContact(
                resourceName=person.google_id,
                body=body,
                updatePersonFields="birthdays",
            )
            .execute()
        )
    except HttpError as e:
        print("🔥 Google responded with an error updating the contact:")
        print(e)
        exit(1)

    updated_person = parse_google_person(result)
    print(f"🎉 Updated {updated_person.name}: {updated_person.birthdate}")


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Annotate google contacts with birthdays."
    )
    parser.add_argument("input", type=str)
    args = parser.parse_args()

    # Parse the person and new birthdate
    person = parse_input(args.input)

    # Authenticate with the google API
    creds = google_auth()
    service = build("people", "v1", credentials=creds)

    try:
        # Find the requested person in the contacts and store the google id
        found_person = find_person(service, person)
        person.name = found_person.name
        person.google_id = found_person.google_id
        person.google_etag = found_person.google_etag

        # Update the birthday
        update_person(service, person)
    except (KeyboardInterrupt, EOFError):
        pass


if __name__ == "__main__":
    main()
