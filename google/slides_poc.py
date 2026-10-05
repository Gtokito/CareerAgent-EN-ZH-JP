from pathlib import Path

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


BASE = Path(__file__).resolve().parent
TOKEN = BASE / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]


def main():
    credentials = Credentials.from_authorized_user_file(
        TOKEN,
        SCOPES,
    )

    slides = build(
        "slides",
        "v1",
        credentials=credentials,
    )

    presentation = slides.presentations().create(
        body={
            "title": "Career Agent R6 PoC"
        }
    ).execute()

    print("Google Slides API: OK")
    print("Presentation ID:", presentation["presentationId"])
    print("Title:", presentation["title"])


if __name__ == "__main__":
    main()
