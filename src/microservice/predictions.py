import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))
from src.data_processing.extract_request_data import get_data_for_model
from src.data_processing.model_utills import load_model


def load_models():
    complex_model = load_model("complex_model")
    simple_model = load_model("simple_model")
    return complex_model, simple_model


complex_model, simple_model = load_models()


def predict(sessions_file: str, tracks_file: str, model: str, month: int):
    data = [get_data_for_model(sessions_file, tracks_file, month)]
    print(data[0])
    if model == "complex":
        return complex_model.predict(data)[0]
    return simple_model.predict(data)[0]


def predict_for_experiment(data: list, model: str):
    data = [data]
    if model == "complex":
        return complex_model.predict(data)[0]
    return simple_model.predict(data)[0]