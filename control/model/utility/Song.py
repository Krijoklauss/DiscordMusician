import discord

class Song:
    def __init__(self, yt_link, pl_link, song_name, dur, views, init_source=False):
        self.youtube_link = yt_link
        self.player_link = pl_link
        self.song_title = song_name
        self.duration = dur
        self.viewCount = views
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10', 
            'options': '-vn -sn'
        }

        if init_source:
            self.audio_source = discord.FFmpegPCMAudio(self.player_link, **self.FFMPEG_OPTIONS)
        else:
            self.audio_source = None

    async def init_audio_source(self):
        self.audio_source = discord.FFmpegPCMAudio(self.player_link, **self.FFMPEG_OPTIONS)
