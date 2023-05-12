import re
import os
import discord
import spotipy
from gtts import gTTS
from pytube import Search
from pytube import YouTube
from pytube import Playlist
from datetime import datetime
from gtts.tts import gTTSError
from gtts.lang import tts_langs
from spotipy import SpotifyClientCredentials
from control.model.utility.Song import Song

spotify = None

def init_apis(host_type: str, database):
    global spotify

    # Spotify API
    spotify_secrets = database.get_spotify_api_secrets(host_type)
    client_credentials_manager = SpotifyClientCredentials(spotify_secrets[0], spotify_secrets[1])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def create_queue(arguments: list) -> list:
    checker = arguments[0]
    is_youtube = "^https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9_-]+).+$"
    is_youtube_playlist = "^https:\/\/www\.youtube\.com\/watch\?v=([A-Za-z0-9_-]+)&list=([A-Za-z0-9_-]+).+$"
    is_spotify_track = "^https:\/\/open\.spotify\.com\/track\/([A-Za-z0-9_-]+)\?si=([A-Za-z0-9]+)$"
    is_spotify_playlist = "^https:\/\/open\.spotify\.com\/playlist\/([A-Za-z0-9_-]+)\?si=([A-Za-z0-9]+)$"
    
    if re.match(is_youtube_playlist, checker):
        return get_youtube_playlist(checker)

    if re.match(is_youtube, checker):
        return get_youtube_song(checker)

    if re.match(is_spotify_track, checker):
        return get_spotify_track(re.match(is_spotify_track, checker).groups()[0])
    
    if re.match(is_spotify_playlist, checker):
        return get_spotify_playlist(checker)

    # Create youtube queue
    queue = ""
    for i, argument in enumerate(arguments):
        if i == len(arguments) - 1:
            queue += argument
        else:
            queue += argument + " "
    return get_youtube_queue(queue)


def get_youtube_song(youtube_link: str) -> list:
    video = YouTube(youtube_link)
    name = video.title
    artist = video.author
    length = video.length
    view_count = video.views
    publish_date = video.publish_date
    return [Song(youtube_link, name, artist, length, clicks=view_count, release=publish_date)]


def get_youtube_playlist(youtube_playlist_link: str) -> list:
    songs = []
    playlist = Playlist(youtube_playlist_link)

    _max_amount = 100
    for i, video in enumerate(playlist.videos):

        # Allow a maximum of 100 Songs from Playlists
        if i >= 100:
            break

        # Get Information
        name = video.title
        artist = video.author
        youtube_link = video.watch_url
        duration = video.length
        songs.append(Song(youtube_link, name, artist, duration))
    return songs


def get_youtube_queue(query: str) -> list:
    video = Search(query).results[0]
    youtube_link = video.watch_url
    name = video.title
    artist = video.author
    length = video.length
    views = video.views
    publish_date = video.publish_date
    return [Song(youtube_link, name, artist, length, clicks=views, release=publish_date)]


def get_spotify_track(spotify_track_id: str) -> list:
    global spotify

    metadata = spotify.track(spotify_track_id)
    return get_youtube_queue(metadata['name'] + " " + metadata['artists'][0]['name'])


def create_tss_file(language: str, tts_string: str) -> tuple or None:
    current_working_directory = os.path.dirname(os.path.abspath(__file__))
    tts_directory = current_working_directory.split('control')[0] + "tts_container\\"
    audio_file_name = str(datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_") + ".mp3"
    audio_file_path = tts_directory + audio_file_name

    # Check if language is supported
    if language not in tts_langs():
        return None

    try:
        speech = gTTS(text=tts_string, lang=language, slow=False)
        speech.save(audio_file_path)
        return discord.FFmpegPCMAudio(audio_file_path), audio_file_path
    except gTTSError:
        os.remove(audio_file_path)
        return None


def delete_tss_file(audio_file_path: str) -> bool:
    try:
        os.remove(audio_file_path)
    except FileNotFoundError:
        return False
    return True


# Currently not supported
def get_spotify_playlist(spotify_playlist_link: str) -> list:
    print("Not supported => " + spotify_playlist_link)
    return []
