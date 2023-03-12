import requests
from bs4 import BeautifulSoup
import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
import pprint


CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")


URL = "https://www.billboard.com/charts/hot-100//" + date

response = requests.get(url=URL)
billboard = response.text

soup = BeautifulSoup(billboard, "html.parser")
songs = soup.select("li h3", id="title-of-a-story")
top_hits = [(song.getText()).strip("\t\n\t\n\t\t\n\t\t\t\t\t") for song in songs]
top_100 = [top_hit for top_hit in top_hits[:100:1]]
# print(top_100)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI, scope="playlist-modify-private",
                                               cache_path="token.txt", show_dialog=True))

user_id = sp.current_user()["id"]
# pprint.pprint(sp.current_user())

uris = []
year = date.split("-")[0]

for song in top_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    # pprint.pprint(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.")


playlist = sp.user_playlist_create(name=f"{date} Billboard 100", user=user_id, public=False)
# pprint.pprint(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=uris)

