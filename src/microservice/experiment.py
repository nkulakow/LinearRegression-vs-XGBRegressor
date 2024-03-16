import requests


def main() -> None:
    artist_data = [
        1761,
        523592344,
        1354,
        1240,
        1840,
        594431109,
        1601,
        1502,
        1975,
        669620295,
        1782,
        1619,
        2251,
        10,
    ]
    data = ("simple", artist_data)
    url = f"http://127.0.0.1:5000/experiment"
    response = requests.post(url, json=data)
    print(response.json().get("prediction"))


if __name__ == "__main__":
    main()