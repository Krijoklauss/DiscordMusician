from control.model.utility.YoutubeUtils import YoutubeUtils
from control.model.utility.SpotifyUtils import SpotifyUtils




class Playlist:
    def __init__(self, playlist_link):
        self.youtube = YoutubeUtils()
        if playlist_link.__contains__("youtube"):
            self.songs = self.youtube.getPlaylistSongs(playlist_link)
        elif playlist_link.__contains__("spotify"):
            self.songs = self.youtube.spotify.spotify_playlist_to_songs(playlist_link)
        else:
            self.songs = [];
