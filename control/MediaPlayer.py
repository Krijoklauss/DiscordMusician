import discord
import asyncio
from control.model.utility.YoutubeUtils import YoutubeUtils
from control.model.utility.Song import Song
from control.LanguageHandler import LanguageHandler

languageHandler = LanguageHandler()
possible_prefixes = ["!", "?", "-", ",", ".", "*", "'", "#", "=", "&", "$", "%", "§", "卐"]


class MediaPlayer:
    def __init__(self, identity, client_name, pref="!", bounded=False, chan="", lang="en"):
        global languageHandler

        self.id = identity
        self.guild = None
        self.client_name = client_name
        self.country_code = lang
        self.language = languageHandler.get_language("en")
        self.prefix = pref
        self.msg_counter = 0
        self.is_bound = bounded
        self.in_queue_loop = False
        self.disconnecting = False
        self.bound_channel = chan
        self.voice_connection = None
        self.song_looped = False
        self.queue_looped = False
        self.skipping = False
        self.current_song = None
        self.current_progress = 0
        self.queue = []
        self.youtube = YoutubeUtils()

    async def send_user_message(self, msg, image=None):
        for channel in self.guild.channels:
            if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                if image is None:
                    await channel.send(msg)
                    return
                else:
                    await channel.send(msg, file=image)
                    return

    async def send_embed(self, e: discord.Embed):
        for channel in self.guild.channels:
                if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                    await channel.send(embed=e)

    async def show_help_message(self):
        helpMessage = "Dies ist eine Liste aller verfügbaren commands und ihrer Anwendung!\n"

        commands = ["prefix", "bind", "nick", "play", "stop", "skip", "pause", "resume", "seek", "np", "queue", "clear", "cleaner", "help"]
        usages = ["*NEW_PREFIX*", "*NEW_TEXTCHANNEL*", "*NEW_NICKNAME*", "*YOUTUBE_LINK*, *SPOTIFY_LINK*, *SOME_WORDS_TO_SEARCH*", "None", "None", "None", "None", "*TIME_TO_SKIP*", "None", "None", "None", "None", "None"]

        for i, command in enumerate(commands):
            helpMessage += self.prefix + command + " | " + usages[i] + "\n"

        _embed = discord.Embed(title="Testing title", description="Some description", color=discord.Color.from_rgb(255, 0, 255))
        _embed.add_field(name="Field1", value="not inline", inline=False)
        _embed.add_field(name="Field2", value="inline", inline=True)
        await self.send_embed(_embed)

        return True, None

    async def set_prefix(self, newPrefix):
        global possible_prefixes

        if possible_prefixes.__contains__(newPrefix):
            self.prefix = newPrefix
            return True, None
        else:
            errorMessage = "Der Prefix befinden sich nicht in unserem Prefix pool!\nUnser Prefix pool sieht wie folgt aus:\n"
            for i, pref in enumerate(possible_prefixes):
                errorMessage += str(i+1) + "." + pref + ",\n"
            return False, errorMessage

    async def set_bind(self, guild, newChannel):
        for channel in guild.channels:
            if type(channel) == discord.TextChannel:
                if channel.name == newChannel:
                    self.is_bound = True
                    self.bound_channel = channel.name
                    return True, None
        return False, "Es tut mir leid aber dieser TEXTKANAL existiert leider nicht auf diesem Server!"

    async def set_nick(self, guild, newNickname):
        nickname = ""
        for name in newNickname:
            nickname += name + " "

        myMember : discord.member = None
        for member in guild.members:
            if member.name == self.client_name:
                myMember = member
                break

        if myMember is None or len(nickname) > 20:
            return False, "Es tut mir leid dieser Name ist zu lang!"

        await myMember.edit(nick=nickname+" "+str(self.prefix)+"prefix")
        return False, "Deine Neuer Nickname lautet: "+str(nickname)

    async def connect(self, channel : discord.channel):
        return await channel.connect(timeout=60, reconnect=True)

    async def play(self, guild: discord.guild, sender: str, args):

        voiceChannel = None
        for channel in guild.channels:
            found = False
            if type(channel) == discord.VoiceChannel:
                for member in channel.members:
                    if member.name == sender:
                        voiceChannel = channel
                        found = True
                        break
                if found: 
                    break

        if voiceChannel is None:
            return False, "VoiceChannel nicht gefunden!"
        
        if self.voice_connection is None or not self.voice_connection.is_connected():
            self.voice_connection = await self.connect(voiceChannel)

        if str(args[0]).__contains__("list"):
            return False, "Under maintenance!"
            newSong = self.youtube.getPlaylistSongs(args[0])
        else:
            newSong = self.youtube.getSong(args)
            self.queue.append(newSong)

        if type(newSong) == tuple:
            return newSong
            
        if self.voice_connection.is_playing() or self.voice_connection.is_paused():
            responseMessage = "Der Song "+str(newSong.song_title)+" wurde der queue hinzugefügt!"
            return False, responseMessage

        if not self.in_queue_loop:
            await self.queue_loop()
        return True, None
        
    async def queue_loop(self):
        self.in_queue_loop = True
        while len(self.queue) > 0:

            currentSong = self.queue.pop(0)

            # Sends special message to channel
            await self.send_user_message("Der Song "+str(currentSong.song_title)+" wird nun abgespielt!")

            self.current_song = currentSong

            if self.voice_connection is not None and self.voice_connection.is_playing():
                self.voice_connection.stop()

            self.voice_connection.play(currentSong.audio_source, after=None)

            while self.current_progress != currentSong.duration:
                await asyncio.sleep(1)

                # Waiting for pause, resume, stop, skip, loop, loopqueue, replay
                if self.voice_connection is None or not self.voice_connection.is_connected():
                    return

                if not self.voice_connection.is_playing() and not self.voice_connection.is_paused():
                    break
                
                if self.skipping:
                    self.skipping = False
                    break

                if self.voice_connection.is_paused():
                    self.current_progress -= 1

                self.current_progress += 1

            self.current_song = None
            self.current_progress = 0

        self.in_queue_loop = False
        await self.stop()
        await self.disconnect()

    async def skip(self):
        if self.voice_connection is not None and self.voice_connection.is_connected() and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            self.skipping = True
            return False, "Aktueller Song übersprungen!"
        return False, "Es wird kein Song abgespielt!"

    async def pause(self):
        if self.voice_connection is not None and self.voice_connection.is_playing():
            self.voice_connection.pause()
            return False, "Aktueller song pausiert!"
        return False, "Es wird kein Song abgespielt!"

    async def resume(self):
        if self.voice_connection is not None and self.voice_connection.is_paused():
            self.voice_connection.resume()
            return False, "Pausierter Song wird nun weiterhin abgespielt!"
        return False, "Es ist kein Song pausiert!"

    async def seek(self, time):
        return False, "Under maintenance!"

        try:
            time = int(time)
        except:
            return False, "Sie müssen eine Zahl zum skippen eingeben!"

        if self.voice_connection is not None and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            # New Timestamp to seek for!
            newTimestamp = (time + self.current_progress)

            if self.current_song.duration <= newTimestamp:
                return False, "Der Song ist kürzer als die Zeit welche Sie skippen möchten!"

            # Insert same song again on 0 queue
            newYoutubeLink = self.current_song.youtube_link + "&t="+str(newTimestamp)
            newSong = self.youtube.getSong(newYoutubeLink)

            if type(newSong) == tuple:
                return newSong

            self.current_song = newSong
            self.voice_connection.source = newSong.audio_source
            self.current_progress = newTimestamp

            return False, "Wir sind zu Sekunde "+str(time)+" gesprungen!"
        return False, "Es wird kein Song abgespielt und es ist auch keiner pausiert!"

    async def stop(self):
        if self.voice_connection is not None and self.voice_connection.is_playing():

            # Empty the current queue
            self.queue = []

            # Stop the MediaPlayer
            self.voice_connection.stop()

            # Sends special message
            await self.send_user_message("Song gestoppt und queue geleert!")

            # Initiate disconnect
            await self.disconnect()
        else:
            return False, "Es wird kein Song abgespielt!"
        return True, None

    async def disconnect(self, delay=60):
        if self.disconnecting:
            return

        self.disconnecting = True
        if self.voice_connection is None:
            await self.voice_connection.disconnect(force=True)

        for i in range(delay):
            if self.voice_connection is not None and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
                self.disconnecting = False
                return

            if i % 20 == 0:
                await self.send_user_message("Disconnecting in "+str(delay-i)+" seconds!")
            await asyncio.sleep(1)

        if self.voice_connection.is_connected() and not self.voice_connection.is_playing() and not self.voice_connection.is_paused():
            await self.voice_connection.disconnect(force=True)
            self.disconnecting = False

    async def show_current_song(self):
        if self.current_song is not None:
            await self.send_user_message("Es wird aktuell " +str(self.current_song.song_title) + ", mit "+str(self.current_song.viewCount) + " Aufrufen abgespielt!")
            return True, None
        else:
            return False, "Kein Song vorhanden!"
    
    async def show_current_queue(self):
        message = ""
        if len(self.queue) > 0:
            for i, song in enumerate(self.queue):
                message += str(i+1) + ". "+str(song.song_title) + ", Aufrufe: "+str(song.viewCount)+"\n"
            await self.send_user_message(message)
            return True, None
        else:
            return False, "Es ist kein Song in der aktuellen queue!"

    async def clear_current_queue(self):
        self.queue = []
        return False, "Die Queue wurde geleert!"

    async def clear_messages(self):
        for channel in self.guild.channels:
            if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                await channel.purge(limit=100)
                return False, "Deleted as many messages as possible!"

    async def change_language(self, code):
        global languageHandler
        if languageHandler.code_exists(code):
            self.language = languageHandler.get_language(code)
            self.country_code = code
            return False, "Changed language to "+str(code)
        else:
            return False, "Country code does not exist!"


