from fastapi import FastAPI, UploadFile, File
from vision_helper import detect_text_from_image_bytes
from firestore_helper import add_dog_food_product, search_products_by_name
import shutil
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# ✅ NEW: Add Product Endpoint
@app.post("/add-product/")
async def add_product(product: dict):
    try:
        add_dog_food_product(product)
        return {"message": "Product added successfully"}
    except Exception as e:
        return {"error": str(e)}
