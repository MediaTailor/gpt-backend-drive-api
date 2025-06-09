from flask import Flask, request, jsonify
from google.oauth2 import service_account
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload
import os

app = Flask(__name__)

# Credenziali da file segreto
credentials = service_account.Credentials.from_service_account_file(
    '/etc/secrets/credentials.json',
    scopes=['https://www.googleapis.com/auth/drive.readonly']
)

drive_service = build('drive', 'v3', credentials=credentials)

@app.route('/read-file', methods=['GET'])
def read_file():
    file_id = request.args.get('file_id')

    if not file_id:
        return jsonify({"error": "Missing 'file_id' parameter"}), 400

    try:
        request_file = drive_service.files().get_media(fileId=file_id)
        file_data = io.BytesIO()
        downloader = MediaIoBaseDownload(file_data, request_file)

        done = False
        while not done:
            status, done = downloader.next_chunk()

        file_data.seek(0)
        content = file_data.read().decode('utf-8')

        return jsonify({"file_id": file_id, "content": content[:4000]})  # Puoi cambiare il limite

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

from flask import send_from_directory

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.well-known', 'ai-plugin.json', mimetype='application/json')
