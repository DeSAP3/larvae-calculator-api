# import base64
import io
# import math
from datetime import datetime

# import cv2
import numpy as np
from flask import Flask, json, jsonify, request, send_file
from flask_cors import CORS
# from loguru import logger
from PIL import Image, ImageDraw

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return "DESAP@2022 API"


@app.route('/calculate/larvae', methods=['POST'])
def calculate_larvae():
    if 'image' not in request.files or 'predictions' not in request.form:
        return jsonify({"error": "No image or predictions part in the request"}), 400

    image_file = request.files['image']
    predictions = json.loads(request.form['predictions'])

    try:
        image = Image.open(image_file)
    except Exception:
        return jsonify({"error": "Invalid image format"}), 400

    draw = ImageDraw.Draw(image)
    for bounding_box in predictions['predictions']:
        if bounding_box['class'] == 'larvae':
            x1 = bounding_box['x'] - bounding_box['width'] / 2
            x2 = bounding_box['x'] + bounding_box['width'] / 2
            y1 = bounding_box['y'] - bounding_box['height'] / 2
            y2 = bounding_box['y'] + bounding_box['height'] / 2
            box = (x1, y1, x2, y2)
            draw.rectangle(box, outline="red", width=5)

    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/jpeg')


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    a = data.get('a')
    b = data.get('b')

    if a is None or b is None:
        return jsonify({"error": "Missing required parameters 'a' and 'b'"}), 400

    try:
        a = float(a)
        b = float(b)
    except ValueError:
        return jsonify({"error": "'a' and 'b' must be numbers"}), 400

    result = a + b

    return jsonify({"result": result})

# @app.route("/calculate-eggs", methods=["POST"])
# def analyzedImage():
#     imageType = request.form.get("imageType")
#     src = request.files.get("src")
#     src = cv2.imdecode(np.fromstring(src.read(), np.uint8), cv2.IMREAD_COLOR)
    
#     # Load Image
#     logger.info("Loading image")
#     if src is None:
#         logger.info("No image selected")
#         logger.error("Exiting program")
#         return
#     overlay = src.copy()
#     logger.info(f'Image shape: {src.shape}')
#     logger.info(f'Image size: {src.size}')
#     logger.info(f'Image dtype: {src.dtype}')
#     logger.success("Loaded image successfully")

#     # Instantiate Constant Matrix
#     threshValue = 0
#     minEggRadius = 0
#     maxEggRadius = 0
#     maxEggCluster = 0
#     logger.info("Instantiating constant matrix")
#     if imageType == 0:
#         threshValue = 116
#         minEggRadius = 1
#         maxEggRadius = 8
#         maxEggCluster = 8
#     elif imageType == 1:
#         threshValue = 120
#         minEggRadius = 5
#         maxEggRadius = 13
#         maxEggCluster = 30
#     else:
#         threshValue = 120
#         minEggRadius = 4
#         maxEggRadius = 14
#         maxEggCluster = 20
#     if threshValue == 0 or minEggRadius == 0 or maxEggRadius == 0 or maxEggCluster == 0:
#         logger.error(
#             f"Invalid constant matrix: {threshValue}, {minEggRadius}, {maxEggRadius}, {maxEggCluster}", style="braces")
#         logger.error("Exiting program")
#         return jsonify({"error": "Error"}), 400
#     logger.success("Instantiated constant matrix successfully")

#     # Preprocess Image
#     logger.info("Preprocessing image")
#     objects = np.zeros((src.shape[0], src.shape[1], 3), dtype=np.uint8)
#     scalar = (255, 255, 255)
#     outlines = np.full(
#         (src.shape[0], src.shape[1], 3), fill_value=scalar, dtype=np.uint8)
#     gray = cv2.cvtColor(src, cv2.COLOR_RGBA2GRAY)
#     _, threshold = cv2.threshold(gray, threshValue, 255, cv2.THRESH_BINARY)
#     M = np.ones((3, 3), dtype=np.uint8)
#     anchor = (-1, -1)
#     dilate = cv2.dilate(threshold, M, anchor, iterations=0,
#                         borderType=cv2.BORDER_CONSTANT)
#     contoursObject = []
#     contoursValues = []
#     contours, hierarchy = cv2.findContours(
#         dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     if gray is None or threshold is None or dilate is None:
#         logger.error("Failed to preprocess image")
#         logger.error("Exiting program")
#         return jsonify({"error": "Error"}), 400
#     logger.success("Preprocessed image successfully")

#     # Analyze Image
#     logger.info("Analyzing image")
#     detectedObjectsArray = []
#     singlesArray = []
#     clustersArray = []
#     singlesCount = 0
#     clustersCount = 0
#     singlesTotalArea = 0
#     clustersTotalArea = 0
#     contoursColor = (255, 255, 255)
#     green = (0, 225, 0, 255)
#     blue = (0, 0, 225, 255)
#     red = (255, 0, 0, 255)
#     grayColor = (100, 100, 100, 255)
#     minEggArea = math.pi * (minEggRadius * minEggRadius)
#     maxEggArea = math.pi * (maxEggRadius * maxEggRadius)
#     maxClusterArea = math.pi * (maxEggCluster * maxEggCluster)

#     for i in range(1, len(contours)):
#         countour = cv2.contourArea(contours[i])
#         contoursObject.append(countour)
#         contoursValues = contoursObject
#         countourMax = max(contoursValues)
#         if countourMax == countour:
#             continue
#         else:
#             cnt = contours[i]
#             rect = cv2.boundingRect(cnt)
#             cv2.drawContours(objects, contours, i,
#                              contoursColor, 1, 8, hierarchy, 100)
#             point1 = (rect[0] - 5, rect[1] - 5)
#             point2 = (rect[0] + rect[2] + 5, rect[1] + rect[3] + 5)
#             if hierarchy[0][i][0] == -1 or hierarchy[0][i][1] == -1 or hierarchy[0][i][2] == -1 or hierarchy[0][i][3] == -1:
#                 cv2.rectangle(objects, point1, point2,
#                               green, 1, cv2.LINE_AA, 0)
#             else:
#                 cv2.rectangle(objects, point1, point2,
#                               green, 3, cv2.LINE_AA, 0)

#             boundingBoxes = src[rect[1]:rect[1] +
#                                 rect[3], rect[0]:rect[0] + rect[2]]
#             detectedObjectsArray.append(boundingBoxes)

#             if countour <= minEggArea:
#                 cv2.drawContours(outlines, contours, i,
#                                  grayColor, -1, cv2.LINE_8, hierarchy, 0)
#                 cv2.drawContours(overlay, contours, i, grayColor,
#                                  1, cv2.LINE_8, hierarchy, 0)
#             elif countour > minEggArea and countour <= maxEggArea:
#                 cv2.drawContours(outlines, contours, i, blue, -
#                                  1, cv2.LINE_8, hierarchy, 0)
#                 cv2.drawContours(overlay, contours, i, blue,
#                                  1, cv2.LINE_8, hierarchy, 0)
#                 singlesArray.append(i)
#                 singlesCount += 1
#             elif countour > maxEggArea and countour <= maxClusterArea:
#                 cv2.drawContours(outlines, contours, i, red, -
#                                  1, cv2.LINE_8, hierarchy, 0)
#                 cv2.drawContours(overlay, contours, i, red,
#                                  1, cv2.LINE_8, hierarchy, 0)
#                 clustersArray.append(i)
#                 clustersCount += 1
#             elif countour > maxClusterArea:
#                 cv2.drawContours(outlines, contours, i,
#                                  grayColor, -1, cv2.LINE_8, hierarchy, 0)
#                 cv2.drawContours(overlay, contours, i, grayColor,
#                                  1, cv2.LINE_8, hierarchy, 0)
#     logger.success("Image analyzed successfully")

#     # Calculate Metrics
#     logger.info("Calculating metrics")
#     singlesTotalArea = sum(singlesArray)
#     singlesAvg = round(singlesTotalArea / len(singlesArray),
#                        2) if singlesArray else 0
#     clustersTotalArea = sum(clustersArray) if clustersCount else 0
#     singlesCalculated = round(
#         clustersTotalArea / singlesAvg) if singlesAvg else 0
#     avgClusterArea = round(clustersTotalArea /
#                            clustersCount, 2) if clustersCount else 0
#     avgEggsPerCluster = round(
#         avgClusterArea / singlesAvg, 1) if singlesAvg else 0
#     totalEggs = singlesCount + singlesCalculated
#     eggEstimate = len(contours)
#     logger.info(f"Singles Average Area: {singlesAvg}")
#     logger.info(f"Singles Calculated: {singlesCalculated}")
#     logger.info(f"Average Cluster Area: {avgClusterArea}")
#     logger.info(f"Average Eggs Per Cluster: {avgEggsPerCluster}")
#     logger.info(f"Total Eggs: {totalEggs}")
#     logger.info(f"Egg Estimate: {eggEstimate}")
#     logger.success("Metrics calculated successfully")

#     retval_threshold, buffer_threshold = cv2.imencode('.jpg', threshold)
#     if retval_threshold:
#         threshold_base64 = base64.b64encode(buffer_threshold).decode('utf-8')
#     else:
#         logger.error("Could not encode threshold image to buffer")
#         return jsonify({"error": "Error"}), 400
        
#     retval_objects, buffer_objects = cv2.imencode('.jpg', objects)
#     if retval_objects:
#         objects_base64 = base64.b64encode(
#             buffer_objects).decode('utf-8')
#     else:
#         logger.error("Could not encode obejcts image to buffer")
#         return jsonify({"error": "Error"}), 400
        
#     retval_outlines, buffer_outlines = cv2.imencode('.jpg', outlines)
#     if retval_outlines:
#         outlines_base64 = base64.b64encode(buffer_outlines).decode('utf-8')
#     else:
#         logger.error("Could not encode outlines image to buffer")
#         return jsonify({"error": "Error"}), 400
        
#     retval_overlay, buffer_overlay = cv2.imencode('.jpg', overlay)
#     if retval_overlay:
#         overlay_base64 = base64.b64encode(buffer_overlay).decode('utf-8')
#     else:
#         logger.error("Could not encode overlay image to buffer")
#         return jsonify({"error": "Error"}), 400

    
#     # return singlesAvg, singlesCalculated, avgClusterArea, avgEggsPerCluster, totalEggs, eggEstimate, threshold, objects, outlines, overlay
#     # threshold_base64 = encode_image_to_base64(threshold)
#     # objects_base64 = encode_image_to_base64(objects)
#     # outlines_base64 = encode_image_to_base64(outlines)
#     # overlay_base64 = encode_image_to_base64(overlay)
    
#     return jsonify({
#         "singlesAvg": singlesAvg,
#         "singlesCalculated": singlesCalculated,
#         "avgClusterArea": avgClusterArea,
#         "avgEggsPerCluster": avgEggsPerCluster,
#         "totalEggs": totalEggs,
#         "eggEstimate": eggEstimate,
#         "threshold": threshold_base64,
#         "objects": objects_base64,
#         "outlines": outlines_base64,
#         "overlay": overlay_base64
#     }), 200


if __name__ == "__main__":
    app.run(debug=True)
