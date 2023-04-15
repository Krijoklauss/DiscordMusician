import math
import discord
import asyncio
from mutagen.mp3 import MP3
from control.model.utility import Values
from control.model.utility import SongFetcher
from control.model.utility.Responses import language_exists
from control.model.utility.Responses import get_language_id
from control.model.utility.Responses import get_language_data
from control.model.utility.Responses import get_language_name
from control.model.utility.Responses import create_discord_response


class Musician:
    def __init__(self, guild_id: int, guild_name: str, client_name: str, nickname="Musician V2 ~ !prefix", prefix="!", bind="", language_id=0) -> None:
        self.guild_id = guild_id
        self.guild_name = guild_name
        self.client_name = client_name
        self.nickname = nickname
        self.voice_connection = None
        self.prefix = prefix
        self.language_id = language_id
        self.bound_channel = bind
        self.queue = []
        self.skipping = False
        self.resuming = False
        self.stopping = False
        self.looping = False
        self.queue_looping = False
        self.disconnecting = False
        self.current_song = None
        self.current_progress = 0

    async def set_bind(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        new_bind = parameter[0]
        for channel in guild.channels:
            if channel.name == str(new_bind) and type(channel) == discord.TextChannel:
                self.bound_channel = channel.name
                return create_discord_response(self.language_id, "bind", "bind_success", values=(self.nickname, self.bound_channel))
        return create_discord_response(self.language_id, "bind", "channel_not_found", values=(str(new_bind)))

    async def set_prefix(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        new_prefix = parameter[0]
        if new_prefix in Values.PREFIXES:
            self.prefix = new_prefix
            await self.set_nick(guild, [self.nickname.split(" ~")[0]], author)
            return create_discord_response(self.language_id, "prefix", "prefix_success", values=(str(new_prefix)))
        else:
            return create_discord_response(self.language_id, "prefix", "prefix_not_allowed", values=(str(new_prefix)))

    async def set_nick(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        new_nickname = ""
        for i, param in enumerate(parameter):
            if i == len(parameter) - 1:
                new_nickname += param
            else:
                new_nickname += param + " "

        # Adding prefix value to nickname
        new_nickname += " ~ " + str(self.prefix) + "prefix"

        # Check parameter error
        if len(new_nickname) > 32:
            return create_discord_response(self.language_id, "nick", "nickname_too_long", values=(str(new_nickname)))
        
        # Search bot member
        for member in guild.members:
            if member.name == self.client_name:
                self.nickname = new_nickname
                await member.edit(nick=new_nickname)
                return create_discord_response(self.language_id, "nick", "nick_success", values=(str(new_nickname)))
        return create_discord_response(self.language_id, "nick", "bot_not_found")

    async def set_default_values(self):
        self.queue = []
        self.skipping = False
        self.resuming = False
        self.stopping = False
        self.looping = False
        self.queue_looping = False
        self.current_song = None
        self.current_progress = 0

    async def connect(self, guild: discord.guild, author: str) -> discord.voice_client or None:
        for channel in guild.channels:
            if type(channel) == discord.VoiceChannel:
                for member in channel.members:
                    if member.name == author:
                        try:
                            return await channel.connect(timeout=60, reconnect=True)
                        except:
                            return self.voice_connection
        return self.voice_connection
                        
    async def play(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed or None:
        self.voice_connection = await self.connect(guild, author)

        created_queue = SongFetcher.create_queue(parameter)
        if len(created_queue) > 0:
            for song in created_queue:
                self.queue.append(song)
                await self.send_to_main_channel(guild, create_discord_response(self.language_id, "play", "added_song", values=(str(song.name))))
        else:
            return create_discord_response(self.language_id, "play", "queue_creation_failed")

        # If already playing don't start a new queue loop
        if self.voice_connection is None:
            return create_discord_response(self.language_id, "play", "bot_not_connected")

        if self.voice_connection is not None and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            return None

        # Currently playing song
        while len(self.queue) > 0:
            
            # Set current song
            self.current_song = self.queue.pop(0)

            # Play audio
            if self.voice_connection is not None and self.voice_connection.is_connected():
                audio_source = self.current_song.init_audio_source()
                if audio_source is None:
                    return create_discord_response(self.language_id, "play", "audio_source_failed")
                await self.send_to_main_channel(guild, create_discord_response(self.language_id, "play", "now_playing", values=(str(self.current_song.name))))
                self.voice_connection.play(audio_source, after=None)
            else:
                return create_discord_response(self.language_id, "play", "bot_not_connected")
            
            # Loop while song is playing
            while self.current_progress <= self.current_song.length:
                # Await second
                await asyncio.sleep(1)

                # disconnect
                if self.voice_connection is None or not self.voice_connection.is_connected():
                    await self.stop(guild, parameter, author)

                # stop
                if self.stopping:
                    self.voice_connection.stop()
                    await self.set_default_values()
                    return create_discord_response(self.language_id, "stop", "stop_success")

                # pause
                if self.voice_connection.is_connected() and self.voice_connection.is_paused():
                    self.current_progress -= 1

                # resume
                if self.voice_connection.is_connected() and self.voice_connection.is_paused() and self.resuming:
                    self.voice_connection.resume()
                    self.resuming = False

                # skip
                if self.skipping:
                    self.skipping = False
                    self.looping = False
                    break

                # After checking add progress
                self.current_progress += 1
        
            # Default 'song is over' values
            self.current_progress = 0

            # Stop audio to prevent errors
            if self.voice_connection.is_connected() and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
                self.voice_connection.stop()

            # Loop
            # Add current song to index 0 in queue
            if self.looping:
                self.queue.insert(0, self.current_song)

            # Loop queue
            # Append current song to the end of the queue
            if self.queue_looping:
                self.queue.append(self.current_song)
        return create_discord_response(self.language_id, "play", "empty_queue")

    async def skip(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.voice_connection is not None and self.voice_connection.is_playing() or self.voice_connection.is_paused():
            self.skipping = True
            return create_discord_response(self.language_id, "skip", "skip_success", values=(str(self.current_song.name)))
        return create_discord_response(self.language_id, "skip", "skip_failed")

    async def resume(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.voice_connection is not None and self.voice_connection.is_paused():
            self.resuming = True
            return create_discord_response(self.language_id, "resume", "resume_success", values=(str(self.current_song.name)))
        return create_discord_response(self.language_id, "resume", "resume_failed")

    async def pause(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.voice_connection is not None and self.voice_connection.is_playing() and not self.voice_connection.is_paused():
            self.voice_connection.pause()
            return create_discord_response(self.language_id, "pause", "pause_success", values=(str(self.current_song.name)))
        return create_discord_response(self.language_id, "pause", "pause_failed")

    async def stop(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed or None:
        if self.voice_connection is not None and self.voice_connection.is_connected() and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            self.stopping = True
            return None
        return create_discord_response(self.language_id, "stop", "stop_failed")

    async def loop(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.queue_looping:
            return create_discord_response(self.language_id, "loop", "loop_failed")
        
        if self.looping:
            self.looping = False
            return create_discord_response(self.language_id, "loop", "loop_passive")
        else:
            self.looping = True
            return create_discord_response(self.language_id, "loop", "loop_active")

    async def loopqueue(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.looping:
            return create_discord_response(self.language_id, "loopqueue", "loopqueue_failed")
        
        if self.queue_looping:
            self.queue_looping = False
            return create_discord_response(self.language_id, "loopqueue", "loopqueue_passive")
        else:
            self.queue_looping = True
            return create_discord_response(self.language_id, "loopqueue", "loopqueue_active")

    # Currently not supported
    async def seek(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        return create_discord_response(self.language_id, "None", "command_not_found", values="seek")

    # Currently not supported
    async def say(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        self.voice_connection = await self.connect(guild, author)
        if self.voice_connection is not None and not self.voice_connection.is_playing() and not self.voice_connection.is_paused():

            # Read parameter
            tts_string = "Failed"
            lang_code = get_language_data(self.language_id)['country_code']
            if parameter[0] == '-l':
                try:
                    lang_code = parameter[1]
                    tts_string = parameter[2]
                except IndexError:
                    return create_discord_response(self.language_id, "say", "say_failed_parameter")
            else:
                tts_string = parameter[0]

            # MP3 File
            sound_data = SongFetcher.create_tss_file(lang_code, tts_string)

            if sound_data is None:
                return create_discord_response(self.language_id, "say", "say_failed_mp3")
            else:
                self.voice_connection.play(sound_data[0])
                await asyncio.sleep(MP3(sound_data[1]).info.length + 1)
                SongFetcher.delete_tss_file(sound_data[1])
                return create_discord_response(self.language_id, "say", "say_success", values=(str(tts_string)))
        else:
            return create_discord_response(self.language_id, "say", "say_failed_music")

    async def show_current_song(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        if self.voice_connection is not None and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            progress_status = ""
            current_progress_percentage = ((self.current_progress * 100) / self.current_song.length)
            cut_percentage = math.floor(current_progress_percentage / 10)
            for p in range(10):
                if p <= cut_percentage:
                    progress_status += "█"
                else:
                    progress_status += "░"
            progress_status += " " + str(round(current_progress_percentage, 2)) + "%"
            cp = (
                self.current_song.youtube_link,
                self.current_song.name,
                self.current_song.artist,
                self.current_song.clicks,
                progress_status,
                self.current_song.release
            )
            return create_discord_response(self.language_id, "show_current_song", "show_current_song_success", values=cp)
        else:
            return create_discord_response(self.language_id, "show_current_song", "show_current_song_failed")

    async def show_queue(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        page = 0
        if len(parameter) > 0:
            try:
                page = int(parameter[0]) - 1
                if page < 0 or page > len(self.queue):
                    return create_discord_response(self.language_id, "queue", "queue_page_not_exists", values=(str(parameter[0])))
            except ValueError:
                return create_discord_response(self.language_id, "queue", "queue_page_not_exists", values=(str(parameter[0])))

        if len(self.queue) < 1:
            return create_discord_response(self.language_id, "play", "empty_queue")

        if len(self.queue) < (page * 25) + 1:
            return create_discord_response(self.language_id, "queue", "queue_page_not_exists", values=(str(parameter[0])))

        queue_string = ""
        _from = page * 25
        _to = (page * 25) + 25
        for i in range(_from, _to):
            position = i + 1
            try:
                song = self.queue[i]
            except IndexError:
                break
            queue_string += str(position) + ". " + song.name + "\n"
        return create_discord_response(self.language_id, "queue", "queue_success", values=(page+1, queue_string))

    async def clear(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        self.queue = []
        return create_discord_response(self.language_id, "clear", "clear_success")
    
    async def clean_channel(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        for channel in guild.channels:
            if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                await channel.purge(limit=100)
                return create_discord_response(self.language_id, "cleaner", "clean_channel_success")
        return create_discord_response(self.language_id, "cleaner", "clean_channel_failed")

    async def show_help(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        helper = ""
        for index, COMMAND in enumerate(Values.COMMANDS, 1):
            helper += str(index) + ". " + str(COMMAND['name']) + "\n"
        return create_discord_response(self.language_id, "help", "help_success", values=(str(helper)))

    async def set_language(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        language = parameter[0]
        if not language_exists(language):
            return create_discord_response(self.language_id, "language", "language_failed")

        self.language_id = get_language_id(language)
        language_name = get_language_name(self.language_id)
        return create_discord_response(self.language_id, "language", "language_success", values=(str(language_name)))

    async def show_languages(self, guild: discord.guild, parameter: list, author: str) -> discord.Embed:
        language_string = ""
        for index, language in enumerate(Values.LANGUAGES, 1):
            language_string += str(index) + ". "+str(language['full_name'])+", CC: " + str(language['country_code']) + "\n"
        return create_discord_response(self.language_id, "languages", "languages_success", values=(str(language_string)))

    async def send_to_main_channel(self, guild: discord.guild, msg: discord.Embed or str) -> None:
        for channel in guild.channels:
            if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                if type(msg) == discord.Embed:
                    await channel.send(embed=msg)
                else:
                    await channel.send(msg)
