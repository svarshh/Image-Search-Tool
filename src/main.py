from PIL import Image
import pytesseract
from pymongo import MongoClient
import hashlib
import os

def get_sha256(image):
    BUF = 128*1024
    sha256 = hashlib.sha256()
    with open(image, 'rb') as f:
        data = f.read(BUF)
        while data:
            sha256.update(data)
            data = f.read(BUF)

    return f"{sha256.hexdigest()}"

def get_images(path):
    images = []
    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith('.png') or f.endswith('jpeg') or f.endswith('.jpg'):
                print(os.path.join(root, f))
                images.append(os.path.join(root, f))
    return images
    

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["texts"]

images = get_images(r'.')

for image in images:
    sha = get_sha256(image)
    doc = list(collection.find({'_id':sha}))
    if not doc:
        text_data = pytesseract.image_to_string(Image.open(image))
        document = {
            "_id" : sha,
            "file_name" : image,
            "data": text_data
        }
        collection.insert_one(document)

print(client.list_database_names())
