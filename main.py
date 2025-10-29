import uvicorn
import os
import shutil
import uuid
import asyncio
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from stego_processor import encode_video, decode_video

app = FastAPI(title="Video Steganography API (Encode/Decode)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORAGE_DIR = os.path.join(BASE_DIR, "storage")
UPLOAD_DIR = os.path.join(STORAGE_DIR, "uploads")
PROCESSED_DIR = os.path.join(STORAGE_DIR, "processed")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Video Steganography API is running. Use /docs for endpoints."}


@app.post("/encode/", tags=["Steganography"])
async def encode(
    file: UploadFile = File(...),
    hidden_text: str = Form(...)
):
    """
    Upload a video + hidden_text -> encode invisibly -> return encoded video.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] or ".mp4"
    upload_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")
    output_name = f"encoded_{job_id}.mp4"
    processed_path = os.path.join(PROCESSED_DIR, output_name)

    try:
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print(f"New encode job {job_id}: text='{hidden_text}'")
        loop = asyncio.get_event_loop()
        out_path = await loop.run_in_executor(None, encode_video, upload_path, processed_path, hidden_text)
        print(f"Encode job {job_id} complete: {out_path}")

        os.remove(upload_path)
        return FileResponse(path=out_path, media_type="video/mp4", filename=os.path.basename(out_path))

    except Exception as e:
        print(f"Error in /encode: {e}")
        raise HTTPException(status_code=500, detail=f"Encode failed: {e}")


@app.post("/decode/", tags=["Steganography"])
async def decode(file: UploadFile = File(...)):
    """
    Decode and reveal hidden text from encoded video.
    """
    job_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] or ".mp4"
    upload_path = os.path.join(UPLOAD_DIR, f"{job_id}{ext}")
    annotated_name = f"decoded_{job_id}.mp4"
    annotated_path = os.path.join(PROCESSED_DIR, annotated_name)

    try:
        with open(upload_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        print(f"New decode job {job_id}")
        loop = asyncio.get_event_loop()
        hidden_data, out_video = await loop.run_in_executor(None, decode_video, upload_path, annotated_path)
        print(f"Decode job {job_id} done.")

        os.remove(upload_path)
        return JSONResponse(status_code=200, content={
            "message": "Decode complete",
            "hidden_text": hidden_data,
            "decoded_video": os.path.basename(out_video)
        })

    except Exception as e:
        print(f"Error in /decode: {e}")
        raise HTTPException(status_code=500, detail=f"Decode failed: {e}")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
