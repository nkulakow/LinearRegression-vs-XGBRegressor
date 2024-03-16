import pandas as pd
import os


DATA_PATH = os.path.join(os.path.dirname(__file__), "../../data/tracks_full_info.jsonl")


def load_data() -> pd.DataFrame:
    with open(DATA_PATH, "r") as file:
        return pd.read_json(file, lines=True)


def aggregate_by_artist(data: pd.DataFrame) -> dict:
    ids = data["id_artist"].unique()
    columns_to_skip = ["id_artist", "track_id", "release_date", "duration_ms"]
    columns = [col for col in data.columns if col not in columns_to_skip]
    aggregated = {artist_id: {col: 0 for col in columns} for artist_id in ids}
    for _, row in data.iterrows():
        artist = row["id_artist"]
        for column in columns:
            aggregated[artist][column] += row[column]
    return aggregated


def aggregate(data: pd.DataFrame) -> dict:
    months_dict = {i + 1: {} for i in range(12)}



def main() -> None:
    data = load_data()
    aggregated = aggregate_by_artist(data)
    no_zero = {}
    for id_ in aggregated.keys():
        for i in range(12):
            if aggregated.get(id_).get(f"time_played_month_{i + 1}") > 0:
                no_zero[id_] = aggregated.get(id_)
                break
    df_data = pd.DataFrame.from_dict(no_zero, orient="index")
    df_data.reset_index(inplace=True)
    df_data = df_data.rename(columns={'index': 'id_artist'})
    df_data.to_json(os.path.join(os.path.dirname(__file__), "../../data/aggregated_2.jsonl"), orient="records", lines=True)


if __name__ == "__main__":
    main()