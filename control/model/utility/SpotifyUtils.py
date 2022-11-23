import re
import spotipy
from control.model.utility.Song import Song
from spotipy import SpotifyClientCredentials


class SpotifyUtils:
    def __init__(self, utils):
        self.youtube = utils
        self.client_id = 'f4a1b01cc3a5426b89d287b03ad37739'
        self.client_secret = '404f71a9280946dd80add3f63009d460'
        self.client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        pass
    
    def spotify_link_to_song(self, link):
        splitter = link.split("/") 
        song_id = splitter[len(splitter)-1]
        meta = self.sp.track(song_id)
        song_name = str(meta['name'])
        artist = str(meta['artists'][0]['name'])
        # album_release = str(meta['album']['release_date'])
        return self.youtube.getSong([artist, song_name])

    def spotify_playlist_to_songs(self, links):
        regex = "https:\/\/open.spotify.com\/playlist\/(\w+)(\??si=\w+)?"
        res = re.match(regex, links)
        playlist_id = res.groups(0)[0]
        playlist = self.sp.playlist(playlist_id=playlist_id)

        tracks = []
        for i, track in enumerate(playlist['tracks']['items'], start=1):
            print("Done with track "+ str(i))
            tracks.append(self.spotify_link_to_song(track['track']['external_urls']['spotify']))
        return tracks
