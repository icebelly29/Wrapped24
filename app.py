import os
import spotipy
import matplotlib.pyplot as plt
import base64
import io
from flask import Flask, redirect, request, session, render_template
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Gonna keep it real its not annual data, its only 6 months

# Load environment variables
load_dotenv()

# Flask and Spotify API Configuration
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify OAuth Configuration
SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'http://localhost:5000/callback'

SCOPE = 'user-top-read user-read-recently-played'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv('SPOTIPY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
        redirect_uri='http://localhost:5000/callback',
        scope='user-top-read user-read-recently-played'
    )

@app.route('/')
def index():
    """Home route to initiate Spotify login"""
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    """Handle Spotify OAuth callback"""
    sp_oauth = create_spotify_oauth()
    session.clear()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session["token_info"] = token_info
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """Generate user's Spotify Wrapped dashboard"""
    # Check if user is authenticated
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect('/')
    
    # Create Spotify client
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Fetch top tracks and artists
    top_tracks = sp.current_user_top_tracks(limit=5, time_range='short_term')
    top_artists = sp.current_user_top_artists(limit=5, time_range='short_term') #6 months actually lol
    
    # Data processing
    track_names = [track['name'] for track in top_tracks['items']]
    track_counts = [track['popularity'] for track in top_tracks['items']]
    
    artist_names = [artist['name'] for artist in top_artists['items']]
    artist_genres = [artist['genres'] for artist in top_artists['items']]
    
    # Flatten genres and count occurrences
    all_genres = [genre for sublist in artist_genres for genre in sublist]
    genre_counts = {}
    for genre in all_genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    # Create visualizations
    # Top Tracks Bar Chart
    plt.figure(figsize=(10, 6))
    plt.bar(track_names, track_counts)
    plt.title('Top Tracks')
    plt.xlabel('Track Name')
    plt.ylabel('Popularity')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    tracks_img = plot_to_base64()
    plt.close()
    
    # Genres Pie Chart
    plt.figure(figsize=(10, 6))
    plt.pie(list(genre_counts.values()), labels=list(genre_counts.keys()), autopct='%1.1f%%')
    plt.title('Top Genres')
    plt.axis('equal')
    genres_img = plot_to_base64()
    plt.close()
    
    return render_template(
        'dashboard.html', 
        top_tracks=top_tracks['items'],
        top_artists=top_artists['items'],
        tracks_chart=tracks_img,
        genres_chart=genres_img
    )

def plot_to_base64():
    """Convert matplotlib plot to base64 encoded image"""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    return f'data:image/png;base64,{image_base64}'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
