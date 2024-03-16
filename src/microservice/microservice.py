from flask import Flask, render_template, request, jsonify
import os
import glob
from predictions import predict, predict_for_experiment
import numpy as np

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main_page():
    def handle_POST():
        sessions_file = request.files["sessions"]
        path = os.path.join(os.path.dirname(__file__), f"uploads/{sessions_file.filename}")
        sessions_file.save(path)

        tracks_file = request.files["tracks"]
        path = os.path.join(os.path.dirname(__file__), f"uploads/{tracks_file.filename}")
        tracks_file.save(path)

        month = int(request.form.get("month"))

        prediction = get_prediction(sessions_file.filename, tracks_file.filename, "simple", month)
        clear_files()
        return render_template("mainpage.html", message=f"model predicted: {int(prediction / 3_600_000)} hours in {month}-th month")

    def handle_GET():
        return render_template("mainpage.html", message="Welcome to IUM prediction service")

    if request.method == "GET":
        return handle_GET()
    return handle_POST()


@app.route("/experiment/", methods=["POST"])
def experiment():
    model, data = request.get_json()
    print("Received data:", data)
    print("Model:", model)
    prediction = predict_for_experiment(data, model)
    serializable_prediction = np.asarray(prediction).astype(float).tolist()
    return jsonify({"prediction": serializable_prediction})


def save_files(files):
    for file in files:
        path = os.path.join(os.path.dirname(__file__), f"uploads/{file.filename}")
        file.save(path)


def get_prediction(sessions_file: str, tracks_file: str, model: str, month: int):
    pred = predict(sessions_file, tracks_file, model, month)
    return pred


def clear_files():
    files_to_remove = glob.glob(os.path.join(os.path.dirname(__file__), "uploads/*.jsonl"))
    for file_path in files_to_remove:
        os.remove(file_path)


if __name__ == "__main__":
    app.run(port=5000)
