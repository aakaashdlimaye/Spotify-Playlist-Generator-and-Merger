from datetime import datetime
import spotipy
import spotipy.util as util
from . import config

def get_user_top_tracks(sp):
    """ Fetch the user's top tracks from Spotify """
    results = sp.current_user_top_tracks(time_range=config.TOP_TRACK_TIME_RANGE,limit=config.TOP_TRACKS_LIMIT)
    top_tracks = []
    for item in results['items']:
        track_id = item['id']
        track_name = item['name']
        print(f"Track ID: {track_id}, Track Name: {track_name}")
        top_tracks.append((track_id, track_name))
    return top_tracks


def create_playlist_and_add_tracks(sp, username, track_ids):
    """ Create a new playlist and add the recommended tracks to it """
    # Get today's date for the playlist title
    today = datetime.today().strftime('%Y-%m-%d')
    playlist_name = f"Recommended Songs on {today}"
    
    # Create the playlist
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True)
    playlist_id = playlist['id']
    
    # Add tracks to the playlist
    sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_ids)
    
    print(f"Playlist '{playlist_name}' created and tracks added successfully!")


def authorize_spotify(username, client_id, client_secret, redirect_uri, scope):
    """Authorize the Spotify API and return a Spotify object"""
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri
    )

    if token:
        sp = spotipy.Spotify(auth=token)
        return sp
    else:
        raise Exception("Failed to retrieve token for Spotify API")