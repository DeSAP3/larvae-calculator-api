from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World!"


@app.route("/test")
def test():
    return "Test API!"


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