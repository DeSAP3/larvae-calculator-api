from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw
import io

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/test")
def test():
    return "Test API!"

@app.route('/calculate/larvae', methods=['POST'])
def calculate_larvae():
    if 'image' not in request.files:
        return "No image provided", 400

    image_file = request.files['image']
    try:
        image = Image.open(image_file)
    except IOError:
        return "Invalid image", 400

    # Annotate the image (for testing, we'll draw a static red rectangle)
    draw = ImageDraw.Draw(image)
    draw.rectangle(((50, 50), (200, 200)), outline="red", width=5)

    # Save the image to a BytesIO object
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

    result = a + b  # Simple example calculation

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)