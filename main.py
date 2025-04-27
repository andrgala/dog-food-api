from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import vision

# ✅ Initialize Firestore and Vision from environment variable
if not firebase_admin._apps:
    firebase_creds_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    if firebase_creds_json:
        creds_dict = json.loads(firebase_creds_json)
        cred = credentials.Certificate(creds_dict)
        firebase_admin.initialize_app(cred)
    else:
        raise Exception("Missing GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable.")

db = firestore.client()
vision_client = vision.ImageAnnotatorClient()

app = FastAPI()

# ✅ Add CORS immediately
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Define Pydantic Model
class ImageUrlRequest(BaseModel):
    imageUrl: str

@app.get("/")
async def root():
    return {"message": "API is live"}

# ✅ Upload endpoint that accepts URL
@app.post("/upload/")
async def upload_image_url(data: ImageUrlRequest):
    try:
        image_url = data.imageUrl
        response = requests.get(image_url)

        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download image.")

        content = response.content

        image = vision.Image(content=content)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        extracted_texts = {
            "brandName": "",
            "productName": "",
            "ingredients": "",
            "feedingGuidelines": ""
        }

        if texts:
            full_text = texts[0].description
            print("Full OCR Text:", full_text)
            extracted_texts["productName"] = full_text.strip()

        return {"extracted_texts": extracted_texts}

    except Exception as e:
        print("Error in upload_image_url:", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Save product endpoint
@app.post("/add-product/")
async def add_product(data: dict):
    try:
        db.collection('dog_food_products').add(data)
        return {"message": "Product saved successfully"}
    except Exception as e:
        print("Error saving product:", str(e))
        raise HTTPException(status_code=500, detail="Failed to save product")

# ✅ Search products endpoint
@app.get("/search-products/")
async def search_products(query: str):
    try:
        products_ref = db.collection('dog_food_products')
        query_ref = products_ref.where('productName', '>=', query).where('productName', '<=', query + '\uf8ff')
        results = query_ref.stream()
        products = [{"id": doc.id, **doc.to_dict()} for doc in results]
        return {"products": products}
    except Exception as e:
        print("Error searching products:", str(e))
        raise HTTPException(status_code=500, detail="Failed to search products")
