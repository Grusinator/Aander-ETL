#!/usr/bin/env python
import argparse

# [START import_client_library]
from google.cloud import vision
# [END import_client_library]
from google.cloud.vision import types
from PIL import Image, ImageDraw



creds = 'AIzaSyBrbIvpN1E17d5ulu-9RhqGHBBcOc5wL9A'

client = vision.ImageAnnotatorClient(credentials=creds)


def detect_labels(face_file):
    client = vision.ImageAnnotatorClient()
    # [END get_vision_service]

    content = face_file.read()
    image = types.Image(content=content)

    return client.label_detection(image=image)


input_filename = "face-input.jpg"

with open(input_filename, 'rb') as image:
    response = detect_labels(image)

    for label in response.label_annotations:
        print("%s : %.2f" %(label.description, label.score))




