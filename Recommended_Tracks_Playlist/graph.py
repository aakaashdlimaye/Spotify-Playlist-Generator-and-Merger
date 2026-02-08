from collections import defaultdict,deque
from .spotify_functions import get_user_top_tracks
import time
from spotipy import SpotifyException
from . import config

class Graph:
    def __init__(self):
        #creates adjacency list
        self.graph = defaultdict(list)

    def add_track(self, track_id):
        if track_id not in self.graph:
            self.graph[track_id] = []

    def add_edge(self, track1, track2):
        if track2 not in self.graph[track1]:
            self.graph[track1].append(track2)
        if track1 not in self.graph[track2]:
            self.graph[track2].append(track1)
    
    def build_graph_from_spotify(self, sp, recommendations_per_song=config.RECOMMENDATION_LIMIT, max_depth=config.GRAPH_MAX_DEPTH,max_requests=config.MAX_REQUESTS,pause_time=config.PAUSE_TIME):
        """
        Build a graph using the user's top tracks and Spotify recommendations
        with depth 3, and a specified number of recommendations per song.
        
        The function stops once 199 requests have been made.
        Utilizes rate limiting: pauses for 1 second after every 5 API requests.
        """
        request_count = 0  # Track the number of API requests made
        node = 0  # Track the number of nodes (tracks) added to the graph
        pause_count = 0 #Track the number of requests without pauses

        def rate_limit_pause():
            nonlocal pause_count
            if pause_count >= 5:
                print(f"Pausing for {pause_time} second to handle rate limiting...")
                time.sleep(pause_time)
                pause_count = 0

        # Step 1: Get the user's top tracks (Depth 0)
        top_tracks = get_user_top_tracks(sp)
        print(f"Retrieved {len(top_tracks)} top tracks")

        # Add the top tracks to the graph (Depth 0)
        for track_id, track_name in top_tracks:
            self.add_track(track_id)
            node += 1  # Increment node count for each top track
            print(f"Added top track {track_name} (Node count: {node})")

        # Track songs at each depth level
        current_depth_tracks = [track_id for track_id, _ in top_tracks]  # Depth 0 (Top tracks)

        # Step 2: Iterate through depths (Depth 1 to Depth 3)
        for depth in range(1, max_depth + 1):
            print(f"Processing depth {depth}...")
            next_depth_tracks = []  # To store tracks for the next depth level

            # Get recommendations for each track in the current depth
            for track_id in current_depth_tracks:
                if request_count >= max_requests:
                    print(f"\nReached the request limit of {max_requests} requests. Stopping further API calls.")
                    return  # Stop if the request limit is reached
                
                try:
                    print(f"Fetching recommendations for track ID: {track_id}")
                    # Get recommendations for the current track
                    recommendations = sp.recommendations(seed_tracks=[track_id], limit=recommendations_per_song)
                    request_count += 1
                    pause_count+=1
                    print(f"Total requests made: {request_count}")
                    rate_limit_pause()  # Apply rate limit after every 5 requests

                    # Process the recommended tracks
                    for rec in recommendations['tracks']:
                        rec_id = rec['id']
                        rec_name = rec['name']
                        print(f"Processing recommendation: {rec_name} (ID: {rec_id})")

                        # Add the recommended track to the graph if not already added
                        self.add_track(rec_id)
                        node += 1  # Increment node count for each recommended track
                        print(f"Added recommended track {rec_name} (Node count: {node})")

                        # Add an edge between the current track and the recommended track
                        self.add_edge(track_id, rec_id)

                        # Store the recommended track for the next depth level
                        next_depth_tracks.append(rec_id)

                except SpotifyException as e:
                    if e.http_status == 429:  # Rate limit hit
                        retry_after = int(e.headers.get("Retry-After", 1))
                        print(f"Rate limit hit, retrying after {retry_after} seconds...")
                        time.sleep(retry_after)
                        request_count = 0  # Reset the request count after waiting
                    else:
                        print(f"Error occurred: {e}")
                        raise

            # Move to the next depth level
            current_depth_tracks = next_depth_tracks

            # If no tracks to explore in the next depth, break early
            if not current_depth_tracks:
                print(f"No more tracks to explore at depth {depth}")
                break

        print(f"Graph building complete with {node} nodes added.")
    
    def bfs_recommendation(self, start_tracks, max_depth=config.BFS_MAX_DEPTH, max_tracks=config.MAX_TRACKS_IN_PLAYLIST,minimum_edges = config.MINIMUM_EDGES):
        """ 
        Perform BFS from multiple start tracks and gather up to max_tracks recommendations,
        but only include tracks that are connected to at least two edges.
        """
        visited = set()  # Tracks already visited
        recommendations = []  # Final list of recommendations
        edge_count = defaultdict(int)  # Count edges for each track
        queue = deque()  # Queue for BFS

        # Initialize the queue with the start tracks at depth 0
        for track in start_tracks:
            queue.append((track, 0))  # (track_id, depth)

        while queue and len(recommendations) < max_tracks:
            current_track, depth = queue.popleft()

            if depth > max_depth:
                continue

            if current_track not in visited:
                visited.add(current_track)

                # Explore neighbors (connected tracks)
                for neighbor in self.graph[current_track]:
                    # Count the number of edges for each neighbor
                    edge_count[neighbor] += 1

                    if neighbor not in visited:
                        queue.append((neighbor, depth + 1))

                # Only add tracks to recommendations if they have at least 2 edges
                if edge_count[current_track] >= minimum_edges and current_track not in start_tracks:
                    recommendations.append(current_track)
                    print(f"Added song {current_track} with edge count {edge_count[current_track]}")

        return recommendations