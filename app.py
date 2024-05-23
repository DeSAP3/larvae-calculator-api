from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw
import io
from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="sP59RbvvS6X3MWqmP5Sq"
)

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


def plot_image(image, result):
    draw = ImageDraw.Draw(image)
    for bounding_box in result['predictions']:
        x1 = bounding_box['x'] - bounding_box['width'] / 2
        x2 = bounding_box['x'] + bounding_box['width'] / 2
        y1 = bounding_box['y'] - bounding_box['height'] / 2
        y2 = bounding_box['y'] + bounding_box['height'] / 2
        box = (x1, y1, x2, y2)
        draw.rectangle(box, outline="red", width=5)
    return image


def image_to_base64(image):
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG')
    img_io.seek(0)
    img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
    return img_base64


@app.route('/calculate/larvae', methods=['POST'])
def calculate_larvae():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    inputImage = request.files['image']
    result = CLIENT.infer(inputImage, model_id="desap/1")

    try:
        requestImage = Image.open(inputImage)
    except IOError:
        return jsonify({"error": "Invalid image"}), 400

    annotated_image = plot_image(requestImage, result)
    annotated_image_base64 = image_to_base64(annotated_image)

    response = {
        "result": result,
        "annotated_image": annotated_image_base64
    }

    return jsonify(response)


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

    result = a + b  # Simple example calculation

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
