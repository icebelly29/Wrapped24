# Spotify Wrapped Clone

## Prerequisites
- Python 3.8+
- Spotify Developer Account

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/spotify-wrapped-clone.git
   cd spotify-wrapped-clone
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Spotify Developer Setup**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Get your Client ID and Client Secret
   - Set Redirect URI to `http://localhost:5000/callback`

5. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```
   SPOTIFY_CLIENT_ID=your_client_id_here
   SPOTIFY_CLIENT_SECRET=your_client_secret_here
   ```

6. **Run the Application**
   ```bash
   python app.py
   ```

7. **Access the App**
   Open `http://localhost:5000` in your browser

## Features
- OAuth 2.0 Authentication with Spotify
- Top Tracks Visualization
- Genre Analysis
- Responsive Dashboard Design

## Technologies
- Flask
- Spotipy
- Matplotlib
- Tailwind CSS

## Future Improvements
- Add more detailed listening statistics
- Implement caching
- Create more advanced visualizations