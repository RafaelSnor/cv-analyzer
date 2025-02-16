import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


SCOPES =['https://www.googleapis.com/auth/drive.file',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/drive.metadata.readonly']

creds = None

if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    print("Credenciales cargadas al archivo token.json")

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        print("credenciales renovadas")
    else:
        print("iniciando el flujo de auth de Oauth...")
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        print("Autorizacion concluida")

    with open('token.json','w') as token:
        token.write(creds.to_json())
        print("Credenciales guardadas en archivo token.json")
