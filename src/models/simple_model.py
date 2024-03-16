import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from sklearn.linear_model import LinearRegression
from src.data_processing.model_utills import get_data_for_model, save_model, load_model


def main() -> None:
    X_train, y_train, X_test, y_test = get_data_for_model()
    model = LinearRegression(fit_intercept=False)
    model.fit(X_train, y_train)
    save_model(model, "simple_model")


if __name__ == "__main__":
    main()
