from PIL import Image
import pytesseract
from pymongo import MongoClient
import hashlib
import os

# return the sha of any given image to check duplicates fast
def get_sha256(image):
    BUF = 128*1024
    sha256 = hashlib.sha256()
    with open(image, 'rb') as f:
        data = f.read(BUF)
        while data:
            sha256.update(data)
            data = f.read(BUF)

    return f"{sha256.hexdigest()}"

# given a path, return all png, jpeg and jpg files
def get_images(path):
    # print(path)
    images = []
    for root, _, files in os.walk(path):
        print(root)
        for f in files:
            print(f)
            if f.endswith('.png') or f.endswith('jpeg') or f.endswith('.jpg'):
                images.append(os.path.join(root, f))
    return images

# given a path, store all the image text data in a database if it doesn't already exist
def store_image_data(path):
    # print("storing")
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    collection = db["texts"]

    images = get_images(path)

    for image in images:
        sha = get_sha256(image)
        doc = list(collection.find({'_id':sha}))
        if not doc:
            print("trying to insert ")
            print(sha)
            text_data = pytesseract.image_to_string(Image.open(image))
            document = {
                "_id" : sha,
                "file_name" : image,
                "data": text_data
            }
            collection.insert_one(document)

# find all the matched words
def check_match(match):

    paths = []

    client = MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    collection = db["texts"]
    images = list(collection.find())

    import re
    for i in images:
        if(re.search(match, i['data'], re.IGNORECASE)):
            paths.append(i['file_name'])
            
    return paths


