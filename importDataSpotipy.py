import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id="54f76f9dd50e4570b70e241d99f45799", client_secret="edc12d92305746419acc63abb418f55a") 
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

uri = "6qqNVTkY8uBg9cP3Jd7DAH"

arista_uri = 'spotify:artist:' + uri

results = sp.artist_albums(arista_uri)

dados = {}
for item in results["items"]:
    print(item["album_group"])
    dados[item["name"]] = []
    for musica in sp._get(item["href"])["tracks"]["items"]:
        duracao = {
            musica["name"]:musica["duration_ms"]
        }
        dados[item["name"]].append(duracao)

#print(dados)
