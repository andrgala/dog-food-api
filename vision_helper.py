import os
import json
from google.cloud import vision
from google.oauth2 import service_account

# Load credentials from environment variable
credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(credentials_info)

# Initialize Vision API client with explicit credentials
client = vision.ImageAnnotatorClient(credentials=credentials)

def detect_text_from_image_bytes(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return ""

    return texts[0].description
