# Spotify API credentials
USERNAME = ""
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8080/callback'
RECOMMENDED_TRACKS_SCOPE = 'user-library-read user-top-read playlist-modify-public'

# Limits
TOP_TRACKS_LIMIT = 10 #the number of tracks that are retreived as base nodes for graph
RECOMMENDATION_LIMIT = 20 #no of recommendations generated per song
BFS_MAX_DEPTH = 2 #depth of bfs
MAX_TRACKS_IN_PLAYLIST = 50 #max no of tracks that will be added to the playlist. BFS stops once this number has been reached
MAX_REQUESTS = 199 #max number of api requests
GRAPH_MAX_DEPTH = 3 #max depth that the graph is built to. starting tracks are considered depth 0
PAUSE_TIME = 1 #seconds between 5 api requests for rate limiting
MINIMUM_EDGES = 2 #the minimum number of edges a song must have to be added to the recommendations playlist

TOP_TRACK_TIME_RANGE = "long_term" 
