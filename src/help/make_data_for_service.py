import os
import pandas as pd


def get_artist_tracks(artist_id: str):
    tracks_ids = []
    tracks_dict = {}
    path = os.path.join(os.path.dirname(__file__), "../../data/tracks.jsonl")
    df_json_reader = pd.read_json(path, lines=True, chunksize=100000)
    for _, df_tracks in enumerate(df_json_reader):
        for _, row in df_tracks.iterrows():
            if row["id_artist"] == artist_id:
                tracks_ids.append(row["id"])
                tracks_dict[row["id"]] = row
    df = pd.DataFrame.from_dict(tracks_dict, orient="index")
    df.to_json(os.path.join(os.path.dirname(__file__), f"../../data/test/{artist_id}_tracks.jsonl"), orient="records",lines=True)
    return tracks_ids


def extract_sessions(artist_id: str, tracks_ids: list[str]):
    path = os.path.join(os.path.dirname(__file__), "../../data/sessions.jsonl")
    df_sessions_json_reader = pd.read_json(path, lines=True, chunksize=100000, dtype={'timestamp': 'str'})
    sessions_dict = {}
    for i, df_sessions in enumerate(df_sessions_json_reader):
        print("Chunk: ", i, end="\r")
        sessions = df_sessions[ df_sessions['event_type'].isin(['play', 'skip', 'like'])].sort_values(by=['session_id', 'timestamp']).to_dict(orient='records')
        index = 0
        while index < len(sessions):
            session = sessions[index]
            month = session["timestamp"][5:7]
            if session["track_id"] in tracks_ids and month >= "07" and month <= "09":
                sessions_dict[session["timestamp"]] = session
            index += 1
    df = pd.DataFrame.from_dict(sessions_dict, orient="index")
    df.to_json(os.path.join(os.path.dirname(__file__), f"../../data/test/{artist_id}_sessions.jsonl"), orient="records",lines=True)


if __name__ == "__main__":
    artist_ids = [
        "3sFhA6G1N0gG1pszb6kk1m",
        "7IAXZaLTb6nkJr8RmVPn5y",
        "51Blml2LZPmy7TTiAg47vQ",
        "5xUf6j4upBrXZPg6AI4MRK",
        "6LuN9FCkKOj5PcnpouEgny",
        "1DTgcOxytJHD8p17mhSgd7",
        "4Z8W4fKeB5YxbusRsdQVPb",
        ]
    artist_id = "4Z8W4fKeB5YxbusRsdQVPb"
    tracks_ids = get_artist_tracks(artist_id)
    extract_sessions(artist_id, tracks_ids)