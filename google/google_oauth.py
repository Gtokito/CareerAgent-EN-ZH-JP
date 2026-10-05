from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow


BASE = Path(__file__).resolve().parent

CREDENTIALS = BASE / "credentials.json"
TOKEN = BASE / "token.json"

SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
]


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS,
        SCOPES,
    )

    credentials = flow.run_local_server(port=0)

    TOKEN.write_text(
        credentials.to_json(),
        encoding="utf-8",
    )

    print("Career Google OAuth: OK")
    print(f"Token: {TOKEN}")


if __name__ == "__main__":
    main()
