from google.cloud import vision
import io
import os

# Load credentials automatically
import json
from google.oauth2 import service_account

credentials_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
credentials = service_account.Credentials.from_service_account_info(credentials_info)

client = vision.ImageAnnotatorClient(credentials=credentials)

client = vision.ImageAnnotatorClient()

def detect_text_from_image_bytes(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return ""

    # texts[0] usually contains all the text detected
    return texts[0].description
