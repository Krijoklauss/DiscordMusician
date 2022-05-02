from control.model.utility.YoutubeUtils import YoutubeUtils

youtube = YoutubeUtils()


class Playlist:
    def __init__(self, playlist_link):
        global youtube

        if playlist_link.__contains__("youtube"):
            self.songs = youtube.getPlaylistSongs(playlist_link)
        else:
            print("Spotify songs")
            self.songs = []