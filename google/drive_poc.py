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

    drive = build(
        "drive",
        "v3",
        credentials=credentials,
    )

    folder = drive.files().create(
        body={
            "name": "Antigravity",
            "mimeType": "application/vnd.google-apps.folder",
        },
        fields="id,name,mimeType",
    ).execute()

    print("Google Drive API: OK")
    print("Folder ID:", folder["id"])
    print("Folder Name:", folder["name"])
    print("MimeType:", folder["mimeType"])


if __name__ == "__main__":
    main()
