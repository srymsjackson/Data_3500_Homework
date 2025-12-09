from dotenv import load_dotenv 
import os
import base64 
from requests import post, get 
import json 
import csv
from datetime import datetime
import time

# Load environment variables
load_dotenv() 

client_id = os.getenv("CLIENT_ID") 
client_secret = os.getenv("CLIENT_SECRET") 

# ==================== AUTHENTICATION ====================

# Obtains our Spotify API Access Token
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
    token = json_result["access_token"] 
    return token

# Returns authorization header with token
def get_auth_header(token):
    return {"Authorization": "Bearer " + token} 

# ==================== DATA COLLECTION ====================

# Searches for an artist
def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    result = get(url + query, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        return None
    return json_result[0]

# Obtains artist's top 10 tracks
def get_artist_top_tracks(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?market=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result.get("tracks", [])

# Details on the artist's info
def get_artist_info(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)

# ==================== GENRE ARTISTS ====================

# Popular artists representing each genre
GENRE_ARTISTS = {
    "Pop": [
        "Taylor Swift", "Ariana Grande", "Dua Lipa", "The Weeknd", "Ed Sheeran",
        "Billie Eilish", "Justin Bieber", "Rihanna", "Bruno Mars", "Lady Gaga",
    ],
    "Hip-Hop": [
        "Drake", "Kendrick Lamar", "Travis Scott", "J. Cole", "21 Savage",
        "Post Malone", "Playboi Carti", "Kanye West", "Doja Cat", "Tyler, The Creator"
    ],
    "Rock": [
        "Coldplay", "Imagine Dragons", "The Killers", "Arctic Monkeys", "Foo Fighters",
        "Linkin Park", "Queen", "The Beatles", "Red Hot Chili Peppers", "Nirvana"
    ],
    "Country": [
        "Morgan Wallen", "Luke Combs", "Chris Stapleton", "Kane Brown", "Carrie Underwood",
        "Zach Bryan", "Cody Johnson", "HARDY", "Cody Jinks", "Thomas Rhett"
    ],
    "Electronic": [
        "David Guetta", "Calvin Harris", "Marshmello", "Kygo", "Martin Garrix",
        "The Chainsmokers", "Avicii", "Alan Walker", "Zedd", "Diplo"
    ],
    "Indie": [
        "Lana Del Rey", "Hozier", "The 1975", "Arctic Monkeys", "Tame Impala",
        "Florence + The Machine", "Lorde", "Mitski", "Phoebe Bridgers", "Mac DeMarco"
    ],
    "Latin": [
        "Bad Bunny", "J Balvin", "Karol G", "Shakira", "Peso Pluma",
        "Ozuna", "Maluma", "Daddy Yankee", "Anuel AA", "Feid",
        "Rauw Alejandro", "Rosalía", "Myke Towers", "Justin Quiles", "Sech"
    ],
    "R&B": [
        "The Weeknd", "SZA", "Frank Ocean", "Summer Walker", "Bryson Tiller",
        "Rihanna", "Doja Cat", "Drake", "H.E.R.", "Jhene Aiko"
    ]
}

# ==================== DATA STORAGE ====================

# Directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Save or append data to CSV file
def save_to_csv(data, filename="genre_data.csv"):
    filepath = os.path.join(SCRIPT_DIR, filename)
    file_exists = os.path.isfile(filepath)
    
    with open(filepath, 'a', newline='', encoding='utf-8') as f:  # Use filepath
        fieldnames = ['date', 'genre', 'artist_name', 'artist_followers', 'artist_popularity', 
                     'track_name', 'track_popularity', 'track_duration_ms', 'explicit']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        for row in data:
            writer.writerow(row)
    
    print(f"Saved {len(data)} tracks to {filename}")


# ==================== MAIN DATA COLLECTION ====================

# Collects popularity data from ALL genre artists
def collect_genre_data(token):
    """Collect popularity data from all genre artists"""
    all_data = []
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    print(f"\nStarting data collection for {current_date}\n")
    
    for genre, artists in GENRE_ARTISTS.items():
        print("Collecting", genre, " data...")
        
        for artist_name in artists:
            try:
                # Search for artist
                artist = search_for_artist(token, artist_name)
                if not artist:
                    print("  (!)  Couldn't find", artist_name)
                    continue
                
                artist_id = artist["id"]
                
                # Get full artist details
                artist_info = get_artist_info(token, artist_id)
                artist_followers = artist_info.get("followers", {}).get("total", 0)
                artist_popularity = artist_info.get("popularity", 0)
                
                # Get top tracks
                top_tracks = get_artist_top_tracks(token, artist_id)
                
                # Store data for each track
                for track in top_tracks:
                    data_row = {
                        "date": current_date,
                        "genre": genre,
                        "artist_name": artist["name"],
                        "artist_followers": artist_followers,
                        "artist_popularity": artist_popularity,
                        "track_name": track["name"],
                        "track_popularity": track["popularity"],
                        "track_duration_ms": track["duration_ms"],
                        "explicit": track.get("explicit", False)
                    }
                    all_data.append(data_row)
                
                print(f"    Got {len(top_tracks)} tracks from {artist_name} (Pop: {artist_popularity}, Followers: {artist_followers:,})")
                time.sleep(0.3)  # Makes the API not wanna end itself!
                
            except Exception as e:
                print(f"  ERROR with {artist_name}: {e}")
                continue
        
        print("  :) Finished", genre, "\n")
    
    return all_data

# ==================== ANALYSIS ====================

# Analyze popularity trends from collected data
def analyze_genre_trends(filename="genre_data.csv"):
    filepath = os.path.join(SCRIPT_DIR, filename)
    if not os.path.isfile(filepath):
        print("(X) No data file found. Run data collection first!")
        return None
    
    # Read all data
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    
    if len(data) == 0:
        print("(X) No data in CSV file!")
        return None
    
    print(f"\n  Analyzing {len(data)} total tracks...\n")
    
    # Group by genre
    genre_stats = {}
    
    # Get column names from first row to handle any naming
    if data:
        columns = data[0].keys()
        print(f"DEBUG: CSV columns: {list(columns)}")
    
    for row in data:
        genre = row['genre']
        if genre not in genre_stats:
            genre_stats[genre] = {
                'track_count': 0,
                'total_track_popularity': 0,
                'total_artist_popularity': 0,
                'total_artist_followers': 0,
                'total_duration': 0,
                'explicit_count': 0,
                'artists': set()
            }
        
        stats = genre_stats[genre]
        stats['track_count'] += 1

        # Handle both possible column names
        track_pop = row.get('track_popularity') or row.get('popularity', 0)
        stats['total_track_popularity'] += int(track_pop)
        stats['total_artist_popularity'] += int(row['artist_popularity'])
        stats['total_artist_followers'] += int(row['artist_followers'])

        # Handle both possible duration column names
        duration = row.get('track_duration_ms') or row.get('duration_ms', 0)
        stats['total_duration'] += int(duration)
        if row['explicit'].lower() == 'true':
            stats['explicit_count'] += 1
        stats['artists'].add(row['artist_name'])
    
    # Calculate averages
    results = {}
    for genre, stats in genre_stats.items():
        count = stats['track_count']
        results[genre] = {
            'tracks_analyzed': count,
            'artists_tracked': len(stats['artists']),
            'avg_track_popularity': round(stats['total_track_popularity'] / count, 2),
            'avg_artist_popularity': round(stats['total_artist_popularity'] / count, 2),
            'avg_artist_followers': round(stats['total_artist_followers'] / count),
            'avg_track_duration_sec': round((stats['total_duration'] / count) / 1000, 1),
            'explicit_percentage': round((stats['explicit_count'] / count) * 100, 1)
        }
    
    # Find most/least popular genres
    sorted_by_track_pop = sorted(results.items(), 
                                 key=lambda x: x[1]['avg_track_popularity'], 
                                 reverse=True)
    
    sorted_by_artist_pop = sorted(results.items(), 
                                  key=lambda x: x[1]['avg_artist_popularity'], 
                                  reverse=True)
    
    analysis_summary = {
        'total_tracks_analyzed': len(data),
        'genres_tracked': list(results.keys()),
        'most_popular_tracks_genre': sorted_by_track_pop[0][0],
        'least_popular_tracks_genre': sorted_by_track_pop[-1][0],
        'most_popular_artists_genre': sorted_by_artist_pop[0][0],
        'genre_with_most_followers': max(results.items(), key=lambda x: x[1]['avg_artist_followers'])[0],
        'longest_tracks_genre': max(results.items(), key=lambda x: x[1]['avg_track_duration_sec'])[0],
        'most_explicit_genre': max(results.items(), key=lambda x: x[1]['explicit_percentage'])[0],
        'genre_statistics': results,
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    return analysis_summary

# Saves our analysis to the results.json file:
def save_results_json(results, filename="results.json"):
    filepath = os.path.join(SCRIPT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    print(f"\n  Results saved to {filename}")

# Prints the results "prettier":
def print_results(results):
    print("\n" + "="*70)
    print("  GENRE POPULARITY TRACKER - RESULTS")
    print("="*70)
    print(f"\n  Total Tracks Analyzed: {results['total_tracks_analyzed']}")
    print(f"  Genres Tracked: {', '.join(results['genres_tracked'])}")
    print(f"\n  HIGHLIGHTS:")
    print(f"    Most Popular Tracks: {results['most_popular_tracks_genre']}")
    print(f"    Most Popular Artists: {results['most_popular_artists_genre']}")
    print(f"    Most Followers: {results['genre_with_most_followers']}")
    print(f"    Longest Tracks: {results['longest_tracks_genre']}")
    print(f"    Most Explicit: {results['most_explicit_genre']}")
    
    print(f"\n  DETAILED STATS BY GENRE:")
    for genre, stats in results['genre_statistics'].items():
        print(f"\n  {genre}:")
        print(f"    • Track Popularity: {stats['avg_track_popularity']}/100")
        print(f"    • Artist Popularity: {stats['avg_artist_popularity']}/100")
        print(f"    • Avg Followers: {stats['avg_artist_followers']:,}")
        print(f"    • Avg Duration: {stats['avg_track_duration_sec']}s")
        print(f"    • Explicit: {stats['explicit_percentage']}%")
    
    print(f"\n (!!)Last Updated: {results['last_updated']}(!!)")
    print("\n" + "="*70 + "\n")

# ==================== MAIN PROGRAM ====================

# Main program execution
def main():
    print("SPOTIFY GENRE POPULARITY TRACKER")
    print("="*70)
    
    # Get token
    token = get_token()
    print("(Authenticated with Spotify API)")
    
    # Collect data
    genre_data = collect_genre_data(token)
    
    if len(genre_data) == 0:
        print("\nNo data collected!")
        return
    
    # Save to CSV
    save_to_csv(genre_data)
    
    # Analyze data
    results = analyze_genre_trends()
    
    if results:
        # Print results
        print_results(results)
        
        # Save to JSON
        save_results_json(results)
        
        print("All done! Run this script again tomorrow to track trends over time.")
        print("(This CSV file will append w/ each run btw!)")
    
if __name__ == "__main__":
    main()