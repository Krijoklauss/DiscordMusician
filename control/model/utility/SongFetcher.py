import re
import os
import discord
import spotipy
from gtts import gTTS
from datetime import datetime
from gtts.tts import gTTSError
from gtts.lang import tts_langs
from youtubesearchpython import Video
from youtubesearchpython import Playlist
from youtubesearchpython import VideosSearch
from spotipy import SpotifyClientCredentials
from control.model.utility.Song import Song

spotify = None


def init_apis(host_type: str, database):
    global spotify

    # Spotify API
    spotify_secrets = database.get_spotify_api_secrets(host_type)
    client_credentials_manager = SpotifyClientCredentials(spotify_secrets[0], spotify_secrets[1])
    spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def parse_duration(duration_string: str) -> int:
    # Calculate video duration
    duration = 0
    length_splitter = duration_string.split(':')
    if len(length_splitter) == 1:
        duration = int(length_splitter[0])
    elif len(length_splitter) == 2:
        seconds = int(length_splitter[1])
        minutes = int(length_splitter[0]) * 60
        duration = seconds + minutes
    elif len(length_splitter) == 3:
        seconds = int(length_splitter[2])
        minutes = int(length_splitter[1]) * 60
        hours = int(length_splitter[0]) * 60 * 60
        duration = seconds + minutes + hours
    return duration


def parse_video_duration(duration_string: str) -> int:
    is_duration = "^PT((\d+)H)*((\d+)M)*((\d+)S)*$"
    groups = re.match(is_duration, duration_string).groups()
    # Hours
    hours = groups[1]
    if hours is None:
        hours = 0
    else:
        hours = int(hours) * 60 * 60
    # Minutes
    minutes = groups[3]
    if minutes is None:
        minutes = 0
    else:
        minutes = int(minutes) * 60
    # Seconds
    seconds = groups[5]
    if seconds is None:
        seconds = 0
    else:
        seconds = int(seconds)
    total_time_in_seconds = hours + minutes + seconds
    return int(total_time_in_seconds)


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
    tries = 0
    video_information = None
    while video_information is None and tries < 3:
        try:
            video_information = Video.get(youtube_link)
        except TypeError:
            pass
        tries += 1
    name = video_information['title']
    artist = video_information['channel']['name']
    length = int(video_information['duration']['secondsText'])
    view_count = int(video_information['viewCount']['text'])
    publish_date = video_information['publishDate']
    return [Song(youtube_link, name, artist, length, clicks=view_count, release=publish_date)]


def get_youtube_playlist(youtube_playlist_link: str) -> list:
    songs = []
    playlist_information = Playlist.get(youtube_playlist_link)
    for video in playlist_information['videos']:
        name = video['title']
        artist = video['channel']['name']
        youtube_link = "https://www.youtube.com/watch?v=" + video['id']
        duration = parse_duration(video['duration'])
        songs.append(Song(youtube_link, name, artist, duration))
    return songs


def get_youtube_queue(query: str) -> list:
    video_search_results = VideosSearch(query, limit=5).result()
    metadata = video_search_results['result'][0]
    youtube_link = "https://www.youtube.com/watch?v=" + str(metadata['id'])
    name = metadata['title']
    artist = metadata['channel']['name']
    length = parse_duration(metadata['duration'])
    views = metadata['viewCount']['short']
    publish_date = metadata['publishedTime']
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
