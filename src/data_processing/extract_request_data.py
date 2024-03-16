import pandas as pd
import os


def aggregate_by_track(sessions: str, tracks: str) -> pd.DataFrame:
    def get_tracks_template(file_name: str) -> dict:
        tracks_path = os.path.join(os.path.dirname(__file__), f"../microservice/uploads/{file_name}")
        print(tracks_path)
        columns_to_read = ["id", "popularity", "duration_ms"]
        df_tracks = pd.read_json(tracks_path, lines=True)[columns_to_read]
        df_tracks["duration_ms"] = df_tracks["duration_ms"].astype("Int64")
        df_tracks["popularity"] = df_tracks["popularity"].astype("Int64")
        track_full_info= df_tracks.set_index("id")[["popularity", "duration_ms"]].to_dict(orient="index")
        for _, value in track_full_info.items():
            for i in range(1, 13):
                value[f'time_played_month_{i}'] = 0
                value[f'likes_month_{i}'] = 0
                value[f'play_without_skip_month_{i}'] = 0
                value[f'play_with_skip_month_{i}'] = 0
        return track_full_info

    def get_aggregated_tracks_info(sessions: str, tracks: str) -> dict:
        track_full_info = get_tracks_template(tracks)
        sessions_path = os.path.join(os.path.dirname(__file__), f"../microservice/uploads/{sessions}")
        df_sessions_json_reader = pd.read_json(sessions_path, lines=True, chunksize=100000)
        for _, df_sessions in enumerate(df_sessions_json_reader):
            sessions = df_sessions[ df_sessions['event_type'].isin(['play', 'skip', 'like'])].sort_values(by=['session_id', 'timestamp']).to_dict(orient='records')
            index = 0
            while index < len(sessions):
                session = sessions[index]
                next_index = index + 1
                if session['event_type'] == 'play':
                    month_number = session['timestamp'].month
                    if next_index < len(sessions) and sessions[next_index]['session_id'] == session['session_id'] and sessions[next_index]['event_type'] == 'skip':
                        track_full_info[session['track_id']][f'time_played_month_{month_number}'] += (sessions[next_index]['timestamp'] - session['timestamp']).total_seconds()*1000
                        track_full_info[session['track_id']][f'play_with_skip_month_{month_number}'] += 1
                        next_index += 1
                    elif next_index < len(sessions) and sessions[next_index]['track_id'] == session['track_id'] and sessions[next_index]['event_type'] == 'like':
                        track_full_info[session['track_id']][f'likes_month_{month_number}'] += 1
                        next_index += 1
                    else:
                        track_full_info[session['track_id']][f'time_played_month_{month_number}'] += track_full_info[session['track_id']]['duration_ms']
                        track_full_info[session['track_id']][f'play_without_skip_month_{month_number}'] += 1
                index = next_index
        return track_full_info

    df = pd.DataFrame.from_dict(get_aggregated_tracks_info(sessions, tracks), orient='index')
    df.reset_index(inplace=True)
    df = df.rename(columns={'index': 'track_id'})
    return df


def aggregate_by_artist(sessions: str, tracks: str) -> pd.DataFrame:
    data = aggregate_by_track(sessions, tracks)
    columns_to_skip = ["track_id", "duration_ms"]
    columns = [col for col in data.columns if col not in columns_to_skip]
    aggregated = {col: 0 for col in columns}
    for _, row in data.iterrows():
        for column in columns:
            aggregated[column] += row[column]
    return pd.DataFrame.from_dict(aggregated, orient="index")[0]


def transform_for_model(data: pd.DataFrame, month: int) -> list:
    new_data = [
        data["popularity"],
        data[f"time_played_month_{month - 3}"],
        data[f"likes_month_{month - 3}"],
        data[f"play_without_skip_month_{month - 3}"],
        data[f"play_with_skip_month_{month - 3}"],
        data[f"time_played_month_{month - 2}"],
        data[f"likes_month_{month - 2}"],
        data[f"play_without_skip_month_{month - 2}"],
        data[f"play_with_skip_month_{month - 2}"],
        data[f"time_played_month_{month - 1}"],
        data[f"likes_month_{month - 1}"],
        data[f"play_without_skip_month_{month - 1}"],
        data[f"play_with_skip_month_{month - 1}"],
        month,
    ]
    return new_data


def get_data_for_model(sessions: str, tracks: str, month: int) -> list:
    aggregated = aggregate_by_artist(sessions, tracks)
    return transform_for_model(aggregated, month)