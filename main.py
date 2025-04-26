from fastapi import FastAPI, UploadFile, File, Query
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io
import cv2
import numpy as np
from firestore_helper import add_dog_food_product, search_products_by_name

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Dog Food API is running!"}

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    try:
        # Read uploaded image into memory
        image_bytes = await image.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Convert to RGB (PIL expects RGB format)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(img_rgb)

        # OCR extraction
        extracted_text = pytesseract.image_to_string(pil_image)

        # Basic fields (simple for now)
        brand_name = "Unknown Brand"
        product_name = "Unknown Product"
        ingredients = extracted_text
        feeding_guidelines = "Feeding guidelines not extracted"

        extracted_texts = {
            "brandName": brand_name,
            "productName": product_name,
            "ingredients": ingredients,
            "feedingGuidelines": feeding_guidelines
        }

        # Save extracted data into Firestore
        add_dog_food_product(extracted_texts)

        return JSONResponse(content={"extracted_texts": extracted_texts})

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/search-products/")
async def search_products(query: str = Query(...)):
    try:
        products = search_products_by_name(query)
        return {"products": products}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
