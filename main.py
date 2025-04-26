from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np

app = FastAPI()

def preprocess_image(img_bytes):
    """Preprocess image for better OCR accuracy without heavy operations."""
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    height, width = img.shape[:2]

    if width < 1000 or height < 1000:
        img = cv2.resize(img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

    return Image.fromarray(thresh)

def run_ocr(image: Image.Image):
    """Run Tesseract OCR with optimized config."""
    custom_config = r'--oem 3 --psm 6'
    return pytesseract.image_to_string(image, config=custom_config)

@app.post("/upload/")
async def upload_image(
    image: UploadFile = File(...)
):
    if not image or not image.filename:
        return JSONResponse(content={"error": "No image uploaded."}, status_code=400)

    image_bytes = await image.read()
    processed_img = preprocess_image(image_bytes)
    extracted_text = run_ocr(processed_img).strip()

    return JSONResponse(content={"extracted_text": extracted_text})
