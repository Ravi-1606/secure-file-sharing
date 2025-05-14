import os
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")

def allowed_file(filename):
    return filename.endswith((".pptx", ".docx", ".xlsx"))

async def save_file(file: UploadFile):
    path = os.path.join(UPLOAD_DIR, file.filename)
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    return path
