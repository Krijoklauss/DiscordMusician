import discord
from youtubesearchpython import Video


class Song:
    def __init__(self, youtube_link: str, name: str, artist: str, length: int, clicks=0, release="01.01.1945") -> None:
        self.name = name
        self.artist = artist
        self.length = length
        self.clicks = clicks
        self.release = release
        self.youtube_link = youtube_link
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10',
            'options': '-vn -sn'
        }

    def fetch_link(self, allowed_opus="audio/webm; codecs=\"opus\"") -> str or None:
        player_link = None
        itag_largest = 0
        tries = 0
        video = None
        while video is None and tries < 3:
            try:
                video = Video.get(self.youtube_link)
            except TypeError:
                pass
            tries += 1

        for form in video['streamingData']['adaptiveFormats']:
            if form['mimeType'] == allowed_opus:
                if form['itag'] > itag_largest:
                    player_link = form['url']
                    itag_largest = form['itag']
        return player_link

    def init_audio_source(self) -> discord.FFmpegPCMAudio or None:
        tries = 0
        max_tries = 3
        player_link = self.fetch_link()
        while player_link is None and tries < max_tries:
            player_link = self.fetch_link()
            tries += 1

        if player_link is None:
            return None

        return discord.FFmpegPCMAudio(player_link, **self.FFMPEG_OPTIONS)
