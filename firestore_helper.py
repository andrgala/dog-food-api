import os
from google.cloud import firestore

# Load Google credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/andreasgalatoulas/cognitail-e29fd163390d.json"

# Initialize Firestore
db = firestore.Client()

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
