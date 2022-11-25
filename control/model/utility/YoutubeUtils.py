from youtubesearchpython import Video
from control.model.utility.Song import Song
from youtubesearchpython import Playlist
from youtubesearchpython import VideosSearch
from youtubesearchpython import StreamURLFetcher
from control.model.utility.SpotifyUtils import SpotifyUtils

class YoutubeUtils:
    def __init__(self):
        self.url_fetcher = StreamURLFetcher()
        self.spotify = SpotifyUtils(self)
        pass

    def getSong(self, args):
        if str(args[0]).__contains__("https://open.spotify.com/track/"):
            return self.spotify.spotify_link_to_song(args[0])
        elif str(args[0]).__contains__("https://www.youtube.com/watch?v="):
            song_link = args[0]
            video = Video.get(song_link)
            videoInfo = Video.getInfo(song_link)
        else:
            # Creating new Query
            query = ""
            for arg in args:
                query += arg + " "

            # Searching for Videos with given query!
            search = VideosSearch(query, limit=5)
            results = search.result()['result']

            # Taking first video found in query
            myVideo = None
            for result in results:
                if result['type'] == 'video':
                    # This is my first best result!
                    myVideo = result
                    break

            if myVideo == None:
                return (1, [query])
            
            song_link = myVideo['link']
            video = Video.get(song_link)
            videoInfo = Video.getInfo(song_link)

        # Last Process is always the same
        if video is None or videoInfo is None:
            return (3, [])

        if int(videoInfo['duration']['secondsText']) > (3600 * 1.5):
            return (2, [videoInfo['title']])

        # Fetch audio streamable url
        player_link = self.url_fetcher.get(video, 251)
        
        return Song(song_link, player_link, videoInfo['title'], int(videoInfo['duration']['secondsText']), videoInfo['viewCount']['text'])

    def getPlaylistSongs(self, playlist_link):
        playlist = Playlist.get(playlist_link)
        
        myList = []
        for i, video in enumerate(playlist['videos']):
            videoId = video['id']
            title = video['title']

            temp = video['duration']
            splitter = temp.split(":")
            temp1 = int(splitter[0]) * 60
            temp2 = splitter [1]
            duration = int(temp1) + int(temp2)
            videoLink = "https://www.youtube.com/watch?v="+str(videoId)

            myList.append(Song(videoLink, None, title, duration, 0))
        return myList

    async def get_player_link(self, youtube_link):
        # Fetch audio streamable url
        video = Video.get(youtube_link)
        player_link = self.url_fetcher.get(video, 251)
        return player_link
