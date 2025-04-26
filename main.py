from fastapi import FastAPI, UploadFile, File
from vision_helper import detect_text_from_image_bytes
from firestore_helper import add_dog_food_product, search_products_by_name
import shutil

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Dog Food API is running!"}

@app.post("/upload/")
async def upload_image(image: UploadFile = File(...)):
    try:
        contents = await image.read()

        # Extract text using Google Vision
        extracted_text = detect_text_from_image_bytes(contents)

        # Here you could add smarter splitting if needed
        # For now just return the whole text
        extracted_texts = {
            "brandName": "",
            "productName": "",
            "ingredients": "",
            "feedingGuidelines": "",
            "fullText": extracted_text
        }

        return {"extracted_texts": extracted_texts}
    except Exception as e:
        return {"error": str(e)}

@app.get("/search-products")
async def search_products(query: str):
    try:
        products = search_products_by_name(query)
        return {"products": products}
    except Exception as e:
        return {"error": str(e)}
