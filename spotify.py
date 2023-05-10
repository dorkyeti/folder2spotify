import os

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from argsparse import args

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRECT = os.getenv('SPOTIFY_CLIENT_SECRET')

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRECT
    )
)

spotify_user = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRECT,
        redirect_uri='http://localhost:3000',
        scope=[
            'playlist-read-private',
            'playlist-read-collaborative',
            'playlist-modify-private',
            'playlist-modify-public'
        ]
    )
)


def search_track(track, limit=1):
    results = spotify.search(
        q="{title} {artist}".format_map(track),
        limit=limit,
        type='track',
        market='VE'
    )

    result = results['tracks']['items']

    if len(result) == 0:
        return None

    return result[0]


def push_tacks_to_playlist(tracks):
    return spotify_user.playlist_add_items(
        args.spotify_playlist_id,
        tracks
    )
