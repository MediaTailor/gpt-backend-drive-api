from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

app = Flask(__name__)

# Autenticazione con il file JSON del Service Account
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file("/etc/secrets/credentials.json")


@app.route('/read-file', methods=['GET'])
def read_file():
    file_name = request.args.get('name')
    if not file_name:
        return jsonify({"error": "Missing 'name' parameter"}), 400

    # Cerca il file nel Drive
    results = drive_service.files().list(
        q=f"name='{file_name}' and mimeType='text/plain'",
        spaces='drive',
        fields='files(id, name)',
        pageSize=1
    ).execute()
    files = results.get('files', [])

    if not files:
        return jsonify({"error": "File not found"}), 404

    file_id = files[0]['id']
    request_file = drive_service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request_file)
    done = False
    while not done:
        _, done = downloader.next_chunk()

    content = fh.getvalue().decode('utf-8')
    return jsonify({
        "file": file_name,
        "content": content[:8000]  # Limite 8000 caratteri per sicurezza
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
