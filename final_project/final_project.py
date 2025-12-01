import os
import json
import base64
from itertools import combinations
from collections import Counter

import pandas as pd
import networkx as nx
from pyvis.network import Network

from dotenv import load_dotenv
from requests import get, post

# ------------------------------------------------------ #
#                   SPOTIFY AUTH                         #
# ------------------------------------------------------ #

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = f"{client_id}:{client_secret}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}

    response = post(url, headers=headers, data=data)
    return response.json()["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

# ------------------------------------------------------ #
#                 SPOTIFY REQUESTS                       #
# ------------------------------------------------------ #

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    
    response = get(url + query, headers=headers).json()
    items = response["artists"]["items"]

    if not items:
        return None
    
    return items[0]

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)

    params = {
        "include_groups": "album,single,compilation,appears_on",
        "limit": 50
    }

    response = get(url, headers=headers, params=params).json()["items"]

    # remove duplicates by album name
    seen = set()
    unique = []
    for album in response:
        name = album["name"].lower()
        if name not in seen:
            seen.add(name)
            unique.append(album)

    return unique

def get_tracks_from_album(token, album_id):
    url = f"https://api.spotify.com/v1/albums/{album_id}/tracks?limit=50"
    headers = get_auth_header(token)
    return get(url, headers=headers).json()["items"]

# ------------------------------------------------------ #
#            COLLABORATION EXTRACTION                    #
# ------------------------------------------------------ #

def extract_collaborations(tracks):
    edges = []
    for track in tracks:
        artist_ids = [a["id"] for a in track["artists"]]
        if len(artist_ids) > 1:
            for pair in combinations(artist_ids, 2):
                edges.append(pair)
    return edges

def get_collaborations_for_artist(token, artist_id):
    albums = get_albums_by_artist(token, artist_id)
    all_edges = []

    for album in albums:
        tracks = get_tracks_from_album(token, album["id"])
        edges = extract_collaborations(tracks)
        all_edges.extend(edges)

    return all_edges

# ------------------------------------------------------ #
#               GRAPH BUILDING + VISUALIZATION           #
# ------------------------------------------------------ #

def build_graph(edges):
    G = nx.Graph()
    weights = Counter(edges)

    for (a1, a2), w in weights.items():
        G.add_edge(a1, a2, weight=w)

    return G, weights

def visualize_graph(G, filename="collab_network.html"):
    nt = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
    nt.force_atlas_2based()  # better layout

    nt.from_nx(G)
    nt.show(filename)

# ------------------------------------------------------ #
#                      MAIN WORKFLOW                     #
# ------------------------------------------------------ #

if __name__ == "__main__":
    token = get_token()

    # Change this to any artist you want
    artist_name = "Sublime"
    
    res = search_for_artist(token, artist_name)
    if res is None:
        print("Artist not found.")
        exit()

    artist_id = res["id"]
    print(f"Building collaboration network for {artist_name}...")

    edges = get_collaborations_for_artist(token, artist_id)

    # Pandas table for inspection
    edges_df = pd.DataFrame(edges, columns=["artist1", "artist2"])
    print("\nSample collaboration edges:")
    print(edges_df.head())

    G, weights = build_graph(edges)

    print("\nGraph stats:")
    print("Nodes:", G.number_of_nodes())
    print("Edges:", G.number_of_edges())

    # Create + auto-open the interactive graph
    visualize_graph(G)
    print("\nInteractive graph saved and opened: collab_network.html")
