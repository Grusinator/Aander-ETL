#!/usr/bin/env python
import argparse

# [START import_client_library]
from google.cloud import vision
# [END import_client_library]
from google.cloud.vision import types
from PIL import Image, ImageDraw
import io

def resize_image(input, max_size):

    pil_img = input

    if pil_img.width > max_size or pil_img.height > max_size:
        if pil_img.height > pil_img.width:
            factor = max_size / pil_img.height
        else:
            factor = max_size / pil_img.width
        m_h = int(pil_img.height * factor)
        m_w = int(pil_img.width * factor)
        #pil_img.resize((m_h, m_w) )

        maxsize = (m_h, m_w)
        print(maxsize)
        pil_img.thumbnail(maxsize, Image.ANTIALIAS)


    imgByteArr = io.BytesIO()
    pil_img.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()

    return imgByteArr






def detect_labels(input_filename, disp=False):

    creds = 'AIzaSyBrbIvpN1E17d5ulu-9RhqGHBBcOc5wL9A'

    client = vision.ImageAnnotatorClient()#credentials=creds)

    #read input file as an image
    #with open(input_filename, 'rb') as image:
    #    content = image.read()


    content = resize_image(Image.open(input_filename), 640)


    #create google type image from input image
    image = types.Image(content=content)

    response = client.label_detection(image=image)

    #for label in response.label_annotations:
    #    print(label.score)

    desc = [l.description for l in response.label_annotations]
    score = [l.score for l in response.label_annotations]

    labels = dict(zip(desc,score))
    if disp:
        for key in labels:
            print("%s : %.2f" %(key, labels[key]))

    return labels




