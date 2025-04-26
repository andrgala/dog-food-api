from google.cloud import vision
import io
import os

# Load credentials automatically
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cognitail-e29fd163390d.json"

client = vision.ImageAnnotatorClient()

def detect_text_from_image_bytes(image_bytes):
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    if not texts:
        return ""

    # texts[0] usually contains all the text detected
    return texts[0].description
