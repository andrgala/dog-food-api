import os
import json
from google.cloud import firestore
from google.oauth2 import service_account

# Get JSON credentials from environment variable
credentials_info = json.loads(os.environ['GOOGLE_APPLICATION_CREDENTIALS_JSON'])

# Create credentials object
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Initialize Firestore client
db = firestore.Client(credentials=credentials, project=credentials.project_id)

def add_dog_food_product(product_data):
    """
    Adds a new dog food product to Firestore
    """
    doc_ref = db.collection("dog_food_products").document()
    doc_ref.set(product_data)

def search_products_by_name(query):
    """
    Search for products by name (simple text match)
    """
    products = []
    docs = db.collection("dog_food_products") \
             .where("productName", ">=", query) \
             .where("productName", "<=", query + "\uf8ff") \
             .stream()
    for doc in docs:
        products.append(doc.to_dict())
    return products
