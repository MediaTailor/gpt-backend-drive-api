from flask import Flask, jsonify, request
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

@app.route("/get-file-content", methods=["GET"])
def get_file_content():
    file_id = request.args.get('id')
    if not file_id:
        return jsonify({"error": "Missing file id"}), 400

    try:
        file = drive_service.files().get_media(fileId=file_id).execute()
        content = file.decode('utf-8')
        return jsonify({"content": content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
