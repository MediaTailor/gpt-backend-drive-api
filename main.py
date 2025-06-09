from flask import Flask, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
SERVICE_ACCOUNT_FILE = '/etc/secrets/credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

drive_service = build('drive', 'v3', credentials=credentials)

@app.route("/list-files", methods=["GET"])
def list_files():
    folder_id = "1F7iioTnfvVZF1uoVQXdO9i5mv32P1NDz"
    query = f"'{folder_id}' in parents and trashed = false"
    results = drive_service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    files = results.get("files", [])
    return jsonify(files)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
