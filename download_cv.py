from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials

def download_files_from_folder(folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('drive', 'v3', credentials=creds)

    results = service.files().list(
        q=f"'{folder_id}' in parents", fields='files(id, name)', supportsAllDrives=True
    ).execute()

    files = results.get('files', [])
    print(files)

    if not files:
        raise FileNotFoundError('No files found in the folder')
    else:
        for file in files:
            requests = service.files().get_media(fileId=file['id'])
            file_path = f"./curriculos/{file['name']}"
            with open(file_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, requests)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
        print("Files downloaded successfully!")

if __name__ == "__main__":
    folder_id = '1PzWYRJmC4jaUIIFdCpKV0UGVMKBdu1fO'
    download_files_from_folder(folder_id)