from .graph import Graph
from .spotify_functions import create_playlist_and_add_tracks, authorize_spotify, get_user_top_tracks
from . import config


def menu():
    sp = authorize_spotify(config.USERNAME, config.CLIENT_ID, config.CLIENT_SECRET, config.REDIRECT_URI, config.RECOMMENDED_TRACKS_SCOPE)

    g = Graph()

    print("\n*** Spotify Custom Playlist Recommendation System ***")
    g.build_graph_from_spotify(sp)
    print("Graph built successfully.")
    
    while True:
        print("\n1. Build playlist from recommendations generated from top 10 songs")
        print("2. Make playlist from your choice of seeds")
        print("3. Exit")
    
        choice = input("Enter your choice: ")

        if choice == "1":
            start_tracks = get_user_top_tracks(sp)
            start_tracks = [track[0] for track in start_tracks[:10]]
            recommendations = g.bfs_recommendation(start_tracks)

            if recommendations:
                print(f"Generated {len(recommendations)} recommendations.")
                print(f"Track IDs: {', '.join(recommendations)}")

                # Create a new playlist and add the recommended tracks
                create_playlist_and_add_tracks(sp, config.USERNAME, recommendations)
            else:
                print("No recommendations found from the given start tracks.")
                
        elif choice == "2":
            n = int(input("Enter number of seed songs (max 10): "))
            start_tracks = []
            for i in range(n):
                track_id = input(f"Enter the track ID for start track {i+1}: ")
                start_tracks.append(track_id)

            # Generate 50 recommended tracks using BFS
            recommendations = g.bfs_recommendation(start_tracks)

            if recommendations:
                print(f"Generated {len(recommendations)} recommendations.")
                print(f"Track IDs: {', '.join(recommendations)}")

                # Create a new playlist and add the recommended tracks
                create_playlist_and_add_tracks(sp, config.USERNAME, recommendations)
            else:
                print("No recommendations found from the given start tracks.")

        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    menu()
