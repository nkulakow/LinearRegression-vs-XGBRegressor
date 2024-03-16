import sys
from pathlib import Path
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.data_processing.model_utills import get_data_for_model, load_model, cross_val_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error


def main() -> None:
    X_train, y_train, X_test, y_test = get_data_for_model()
    model = load_model("complex_model")
    y_pred = model.predict(X_test)

    errors = []
    for i in range(len(X_test)):
        perc_error = abs(y_test[i] - y_pred[i]) / y_test[i]
        errors.append(perc_error)
        print(f"true value: {y_test[i]}, predicted value: { y_pred[i]}")

    print(f"mae: {mean_absolute_error(y_test, y_pred)}")
    print(f"perc_error: {sum(errors)/len(errors)}")
    print(f"r2_score: {r2_score(y_test, y_pred)}")

    # Walidacja krzyżowa
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="r2")
    # Średnia ocena R-squared z walidacji krzyżowej
    average_r2 = cv_scores.mean()
    print(f"Average R-squared: {average_r2}")
    # save_model(model)


if __name__ == "__main__":
    main()
