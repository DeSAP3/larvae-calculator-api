import io
from flask import Flask, json, jsonify, request, send_file
from flask_cors import CORS
from PIL import Image, ImageDraw

app = Flask(__name__)
CORS(app)
@app.route("/")
def home():
    return "Hello World!"

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


if __name__ == "__main__":
    app.run(debug=True)
