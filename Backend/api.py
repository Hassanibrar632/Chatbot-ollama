from flask import Flask, request, jsonify
import os
import uuid
import subprocess
from pathlib import Path

app = Flask(__name__)
UPLOAD_DIR = "uploads"

@app.route("/upload/", methods=["POST"])
def upload_files():
    try:
        if 'files' not in request.files:
            return jsonify({"error": "No files provided."}), 400

        files = request.files.getlist("files")
        print(f"Received {len(files)} files:")
        for f in files:
            print(f.filename)

        # Generate a unique folder name
        folder_name = str(uuid.uuid4())
        folder_path = Path(UPLOAD_DIR) / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        
        file_details = []
        for file in files:
            file_path = folder_path / file.filename
            file.save(file_path)
            file_details.append({"filename": file.filename, "path": str(file_path)})
        
        # Start a subprocess to execute a script with sleep_time as argument
        script_path = Path("Preprocess.py").absolute()
        subprocess.Popen(["python", str(script_path), "1"], shell=True)

        return jsonify({"folder": folder_name, "file_count": len(files), "files": file_details})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
