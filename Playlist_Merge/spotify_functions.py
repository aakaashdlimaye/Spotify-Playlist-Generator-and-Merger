import spotipy
import spotipy.util as util
from . import config
from .linked_list import LinkedList


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
    

def get_tracks_from_playlist(sp, playlist_id, username = config.USERNAME):
    ''' 
    Given a Spotipy object, a username, and a playlist_id,
    returns a LinkedList of all the track ids in the playlist.
    '''
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = LinkedList()  # Using LinkedList instead of a Python list
    
    for t in results['items']:
        tracks.append(t['track']['id'])

    while results['next']:
        results = sp.next(results)
        for t in results['items']:
            tracks.append(t['track']['id'])

    return tracks

def divide_chunks(track_list, n):
    '''
    Given a list, it divides it into a list of lists,
    each of them with a length less or equal to n.
    '''
    for i in range(0, len(track_list), n):
        yield track_list[i:i + n]

def binary_search(sorted_list, target):
    """Perform binary search for a target in a sorted list."""
    low = 0
    high = len(sorted_list) - 1

    while low <= high:
        mid = (low + high) // 2
        if sorted_list[mid] == target:
            return True
        elif sorted_list[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return False