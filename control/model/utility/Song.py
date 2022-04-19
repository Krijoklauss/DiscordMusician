import discord

class Song:
    def __init__(self, yt_link, pl_link, song_name, dur, views):
        self.youtube_link = yt_link
        self.player_link = pl_link
        self.song_title = song_name
        self.duration = dur
        self.viewCount = views

        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 10', 
            'options': '-vn -sn'
        }
        self.audio_source = discord.FFmpegPCMAudio(self.player_link, **FFMPEG_OPTIONS)
