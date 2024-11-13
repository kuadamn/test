from dotenv import load_dotenv
import os 
import base64
from requests import get, post
import json
import webbrowser

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    if "access_token" in json_result:
        return json_result["access_token"]
    else:
        print("Error: 'access_token' not found in the response.")
        return None

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def search_for_artist(token, artist_name) :
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists...")
        return None
    
    return(json_result)[0]
    
def get_songs_by_artist(token, artist_id) :
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers = headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def play_song_on_spotify(song_uri) :
    webbrowser.open(song_uri)

name = input("Artist name: ")
token = get_token()
result = search_for_artist(token, name)
artist_id = result["id"]
songs = get_songs_by_artist(token,artist_id)

print("Closest Match: " + result["name"])
for idx, song in enumerate(songs):
    print(f"{idx + 1} . {song['name']}")

queued_song = input("Which song would you like to play? (Press 1-10 to select song. Press any other key to exit.):")

if queued_song.isdigit():
    song_index = int(queued_song) - 1
    if 0 <= song_index < len(songs):
        song_uri = songs[song_index]['uri']
        print(f"Playing : {songs[song_index]['name']}")
        play_song_on_spotify(song_uri)
    else :
        print("Exiting the program..")


