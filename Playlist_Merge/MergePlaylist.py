from .linked_list import LinkedList
from . import config
from .spotify_functions import authorize_spotify, divide_chunks, get_tracks_from_playlist,binary_search

def playlist_union(username = config.USERNAME):
    sp = authorize_spotify(config.USERNAME, config.CLIENT_ID, config.CLIENT_SECRET, config.REDIRECT_URI, config.SCOPE)

    destination_playlist = input("Enter the destination playlist ID: ")
    source_playlists = input("Enter the source playlist IDs (comma-separated): ").split(',')

    destination_playlist_tracks = get_tracks_from_playlist(sp,destination_playlist)
    destination_tracks_list = destination_playlist_tracks.to_list()
    destination_tracks_list.sort()

    for playlist in source_playlists:
        tracks = get_tracks_from_playlist(sp, playlist)
        track_list = tracks.to_list()  # Convert LinkedList to list for easier handling
        
        # Initialize an empty list to hold tracks that aren't already in the destination playlist
        filtered_tracks = []

        # Use binary search to check if each track from the source playlist exists in the destination playlist
        for track in track_list:
            if not binary_search(destination_tracks_list,track):
                filtered_tracks.append('spotify:track:' + track)
                destination_tracks_list.append(track)
                destination_tracks_list.sort()

        if filtered_tracks:
            # We can add only 100 tracks at a time, so the list of track ids is divided
            tracks_chunks = divide_chunks(filtered_tracks, 100)
            for chunk in tracks_chunks:
                sp.user_playlist_add_tracks(username, destination_playlist, chunk)
            print("Added tracks!")
        else:
            print("No tracks to add!")


if __name__ == "__main__":
    playlist_union()