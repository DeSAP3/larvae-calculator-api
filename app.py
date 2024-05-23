from flask import Flask, request, jsonify
from PIL import Image, ImageDraw

# Opening the image to be used
img = Image.open('img_path.png')

# Creating a Draw object
draw = ImageDraw.Draw(img)

# Drawing a green rectangle
# in the middle of the image
draw.rectangle(xy=(50, 50, 150, 150),
               fill=(0, 127, 0),
               outline=(255, 255, 255),
               width=5)

# Method to display the modified image
img.show()

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/test")
def test():
    return "Test API!"

@app.route('/calculate/larvae')
def calculate_larvae(image):
    img = Image.open(image)
    draw = ImageDraw.Draw(img)
    draw.rectangle(xy=(50, 50, 150, 150),
                   fill=(0, 127, 0),
                   outline=(255, 255, 255),
                   width=5)
    img.show()
    


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