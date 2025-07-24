
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import List

app = FastAPI()

UPLOAD_DIR = "uploaded_docs"
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large. 10MB max.")
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    return JSONResponse(status_code=201, content={
        "filename": file.filename,
        "size": len(contents),
        "message": "File uploaded successfully."
    })
