import pandas as pd
import os
import pickle
from sklearn.model_selection import cross_val_score

MONTH = 10


def save_model(model, file_name: str):
    path = os.path.join(os.path.dirname(__file__), f"../models/{file_name}.pkl")
    with open(path, "wb") as model_file:
        pickle.dump(model, model_file)


def load_model(file_name):
    path = os.path.join(os.path.dirname(__file__), f"../models/{file_name}.pkl")
    with open(path, "rb") as model_file:
        return pickle.load(model_file)


def get_data():
    with open(os.path.join(os.path.dirname(__file__), "../../data/aggregated.jsonl"), "r") as file:
        return pd.read_json(file, lines=True)


def get_columns():
    """Columns in X data"""
    return [
        "poularity",
        "time_played_3_months_before",
        "likes_3_months_before",
        "play_without_skip_3_months_before",
        "play_with_skip_3_months_before",
        "time_played_2_month_before",
        "likes_2_months_before",
        "play_without_skip_2_months_before",
        "play_with_skip_2_months_before",
        "time_played_1_month_before",
        "likes_1_month_before",
        "play_without_skip_1_month_before",
        "play_with_skip_1_month_before",
        "month_to_predict",
    ]


def get_train_data(data: pd.DataFrame) -> pd.DataFrame:
    new_data = []
    for _, row in data.iterrows():
        for i in range(4, MONTH):
            row_data = {
                "popularity": row["popularity"],
                "time_played_3_months_before": row[f"time_played_month_{i - 3}"],
                "likes_3_months_before": row[f"likes_month_{i - 3}"],
                "play_without_skip_3_months_before": row[f"play_without_skip_month_{i - 3}"],
                "play_with_skip_3_months_before": row[f"play_with_skip_month_{i - 3}"],
                "time_played_2_month_before": row[f"time_played_month_{i - 2}"],
                "likes_2_months_before": row[f"likes_month_{i - 2}"],
                "play_without_skip_2_months_before": row[f"play_without_skip_month_{i - 2}"],
                "play_with_skip_2_months_before": row[f"play_with_skip_month_{i - 2}"],
                "time_played_1_month_before": row[f"time_played_month_{i - 1}"],
                "likes_1_month_before": row[f"likes_month_{i - 1}"],
                "play_without_skip_1_month_before": row[f"play_without_skip_month_{i - 1}"],
                "play_with_skip_1_month_before": row[f"play_with_skip_month_{i - 1}"],
                "month_to_predict": i,
                "time_played_to_predict": row[f"time_played_month_{i}"],
            }
            new_data.append(row_data)
    return pd.DataFrame(new_data)


def get_test_data(data: pd.DataFrame) -> pd.DataFrame:
    new_data = []
    for _, row in data.iterrows():
        for month in range(MONTH, 12):
            row_data = {
                "popularity": row["popularity"],
                "time_played_3_months_before": row[f"time_played_month_{month - 3}"],
                "likes_3_months_before": row[f"likes_month_{month - 3}"],
                "play_without_skip_3_months_before": row[f"play_without_skip_month_{month - 3}"],
                "play_with_skip_3_months_before": row[f"play_with_skip_month_{month - 3}"],
                "time_played_2_month_before": row[f"time_played_month_{month - 2}"],
                "likes_2_months_before": row[f"likes_month_{month - 2}"],
                "play_without_skip_2_months_before": row[f"play_without_skip_month_{month - 2}"],
                "play_with_skip_2_months_before": row[f"play_with_skip_month_{month - 2}"],
                "time_played_1_month_before": row[f"time_played_month_{month - 1}"],
                "likes_1_month_before": row[f"likes_month_{month - 1}"],
                "play_without_skip_1_month_before": row[f"play_without_skip_month_{month - 1}"],
                "play_with_skip_1_month_before": row[f"play_with_skip_month_{month - 1}"],
                "month_to_predict": month,
                "time_played_to_predict": row[f"time_played_month_{month}"],
            }
            new_data.append(row_data)
    return pd.DataFrame(new_data)


def get_data_for_model() -> tuple:
    data = get_data()

    train_data = get_train_data(data)
    train_data_list = [(row.to_list()[:-1], row.to_list()[-1]) for _, row in train_data.iterrows()]
    X_train = [exmpl[0] for exmpl in train_data_list]
    y_train = [exmpl[1] for exmpl in train_data_list]

    test_data = get_test_data(data)
    test_data_list = [(row.to_list()[:-1], row.to_list()[-1]) for _, row in test_data.iterrows()]
    X_test = [exmpl[0] for exmpl in test_data_list]
    y_test = [exmpl[1] for exmpl in test_data_list]

    return X_train, y_train, X_test, y_test


def get_cv_score_mae(model, X, y):
    cv_scores = cross_val_score(model, X, y, cv=5, scoring="neg_mean_absolute_error")
    average_mae = cv_scores.mean()
    return average_mae
