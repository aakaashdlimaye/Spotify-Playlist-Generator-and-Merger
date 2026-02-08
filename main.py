from Playlist_Merge.MergePlaylist import playlist_union
from Recommended_Tracks_Playlist.RecommendedSongsPlaylist import menu


while True:

    print("\n\n\n******Welcome to Spotify Merge and Recommend******")
    print("1. Merge Playlists")
    print("2. Create playlist from recommended tracks")
    print("3. Exit")
    choice = input("Enter your choice: ")

    if choice == "1":
        playlist_union()
    elif choice == '2':
        menu()
    elif choice == '3':
        print("Exiting... ")
        break
    else:
        print("Enter a valid choice\n\n")