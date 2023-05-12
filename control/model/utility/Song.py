import discord
from pytube import YouTube
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
        audio = YouTube(self.youtube_link).streams.get_audio_only()
        return audio.url

    def init_audio_source(self) -> discord.FFmpegPCMAudio or None:
        player_link = self.fetch_link()
        if player_link is None:
            return None

        return discord.FFmpegPCMAudio(player_link, **self.FFMPEG_OPTIONS)
