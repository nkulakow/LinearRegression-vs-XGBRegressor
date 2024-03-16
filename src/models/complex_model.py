import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from xgboost import XGBRegressor
from src.data_processing.model_utills import get_data_for_model, save_model


def main() -> None:
    X_train, y_train, X_test, y_test = get_data_for_model()
    model = XGBRegressor(learning_rate=0.2)
    model.fit(X_train, y_train)
    save_model(model, "complex_model")


if __name__ == "__main__":
    main()
