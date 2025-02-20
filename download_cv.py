from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import os
from dotenv import load_dotenv
load_dotenv()

def get_credentials():
    """Obtiene credenciales desde variables de entorno en Render"""
    client_id = os.getenv("GOOGLE_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    refresh_token = os.getenv("GOOGLE_REFRESH_TOKEN")
    token_uri = os.getenv("GOOGLE_TOKEN_URI")

    creds_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "token_uri": token_uri
    }
    return Credentials.from_authorized_user_info(creds_data)

def download_files_from_folder(folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
    creds = get_credentials()
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents", fields='files(id, name)', supportsAllDrives=True
    ).execute()

    files = results.get('files', [])

    if not files:
        raise FileNotFoundError('No files found in the folder')

    curriculos_dir = "./curriculos"
    if not os.path.exists(curriculos_dir):
        os.makedirs(curriculos_dir)

    for file in files:
        request = service.files().get_media(fileId=file['id'])
        file_path = os.path.join(curriculos_dir, file['name'])

        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()

        print(f"Archivo descargado: {file['name']}")

if __name__ == "__main__":
    folder_id = '1PzWYRJmC4jaUIIFdCpKV0UGVMKBdu1fO'
    download_files_from_folder(folder_id)
