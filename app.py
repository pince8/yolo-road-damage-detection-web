from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os

from utils.detector import detect_image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict-ui", methods=["POST"])
def predict_ui():
    if "image" not in request.files:
        return "No image uploaded", 400

    file = request.files["image"]
    filename = secure_filename(file.filename)

    input_path = os.path.join(UPLOAD_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    file.save(input_path)

    detect_image(input_path, output_path)

    return render_template(
        "index.html",
        output_image=f"results/{filename}"
    )

if __name__ == "__main__":
    app.run(debug=True)
