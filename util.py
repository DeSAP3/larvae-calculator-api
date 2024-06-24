import base64
import cv2
import numpy as np


def encode_image_to_base64(image_array):
    retval, buffer = cv2.imencode('.jpg', image_array)
    if retval:
        base64_str = base64.b64encode(buffer).decode('utf-8')
        return base64_str
    else:
        raise ValueError("Could not encode image to buffer")

def instantiateConstMatrix(imageType):
    if imageType == 0:
        threshValue = 116
        minEggRadius = 1
        maxEggRadius = 8
        maxEggCluster = 8
        return threshValue, minEggRadius, maxEggRadius, maxEggCluster
    elif imageType == 1:
        threshValue = 120
        minEggRadius = 5
        maxEggRadius = 13
        maxEggCluster = 30
        return threshValue, minEggRadius, maxEggRadius, maxEggCluster
    else:
        threshValue = 120
        minEggRadius = 4
        maxEggRadius = 14
        maxEggCluster = 20
        return threshValue, minEggRadius, maxEggRadius, maxEggCluster
