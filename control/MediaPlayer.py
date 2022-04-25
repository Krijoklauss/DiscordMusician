import discord
import asyncio
from control.model.utility.YoutubeUtils import YoutubeUtils
from control.model.utility.Song import Song
from control.LanguageHandler import LanguageHandler
from control.model.utility.Playlist import Playlist


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

    async def create_embed_message(self, embedResponse, replacements):
        title = embedResponse['title']
        description = embedResponse['description']
        color = embedResponse['color']

        msg = discord.Embed(title=title, description=description, color=discord.Color.from_rgb(color[0], color[1], color[2]))
        for i, field in enumerate(embedResponse['fields']):
            try:
                name = field['name']
            except (IndexError, KeyError):
                return msg

            try:
                replacement = replacements[i]
                msg.add_field(name=field['name'], value=field['value'] % replacement, inline=field['inline'])
            except (IndexError, KeyError):
                msg.add_field(name=field['name'], value=field['value'], inline=field['inline'])
        return msg

    async def send_embed(self, e: discord.Embed):
        for channel in self.guild.channels:
                if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                    await channel.send(embed=e)

    async def show_help_message(self):
        myLanguage = self.language['commands']['help']

        commands = ["prefix", "bind", "nick", "play", "stop", "skip", "pause", "resume", "seek", "np", "queue", "clear", "cleaner", "help", "lang"]
        usages = ["*NEW_PREFIX*", "*NEW_TEXTCHANNEL*", "*NEW_NICKNAME*", "*YOUTUBE_LINK*, *SPOTIFY_LINK*, *SOME_WORDS_TO_SEARCH*", None, None, None, None, "*TIME_TO_SKIP*", None, None, None, None, None, "*COUNTRY_CODE*"]

        myEmbed = await self.create_embed_message(myLanguage['works'], [])
        for i, command in enumerate(commands):
            v = usages[i]
            if v is None:
                myEmbed.add_field(name=command, value="No arguments required!", inline=False)
            else:
                myEmbed.add_field(name=command, value=v, inline=False)

        await self.send_embed(myEmbed)
        return True, None

    async def set_prefix(self, newPrefix):
        global possible_prefixes

        myLanguage = embedResponseJson = self.language['commands']['prefix']

        if possible_prefixes.__contains__(newPrefix):
            oldPrefix = self.prefix
            self.prefix = newPrefix

            await self.send_embed(await self.create_embed_message(myLanguage["works"], [newPrefix, oldPrefix]))
            return True, None
        else:
            prefixPool = ""
            for i, pref in enumerate(possible_prefixes):
                prefixPool += str(i+1) + "." + pref + ",\n"

            replacements = [prefixPool]
            embedResponseJson = myLanguage["fails"][0]
            return False, await self.create_embed_message(embedResponseJson, replacements)

    async def set_bind(self, guild, newChannel):

        myLanguage = self.language['commands']['bind']
        for channel in guild.channels:
            if type(channel) == discord.TextChannel:
                if channel.name == newChannel:

                    self.is_bound = True
                    self.bound_channel = channel.name

                    await self.send_embed(await self.create_embed_message(myLanguage["works"], [newChannel, self.bound_channel]))
                    return True, None
    
        return False, await self.create_embed_message(myLanguage["fails"][0], [newChannel])

    async def set_nick(self, guild, newNickname):
        nickname = ""
        for name in newNickname:
            nickname += name + " "

        myMember : discord.member = None
        for member in guild.members:
            if member.name == self.client_name:
                myMember = member
                break
        
        myLanguage = self.language['commands']['nick']
        if myMember is None:
            return False, await self.create_embed_message(myLanguage['fails'][0], [])

        if len(nickname) > 35:
            return False, await self.create_embed_message(myLanguage['fails'][1], [])

        await myMember.edit(nick=nickname+" "+str(self.prefix)+"prefix")
        await self.send_embed(await self.create_embed_message(myLanguage['works'], [nickname]))

        return True, None

    async def connect(self, channel : discord.channel):
        return await channel.connect(timeout=60, reconnect=True)

    async def play(self, guild: discord.guild, sender: str, args):

        myLanguage = self.language['commands']['added_to_queue']
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
            return False, await self.create_embed_message(myLanguage['fails'][0], [])
        
        if self.voice_connection is None or not self.voice_connection.is_connected():
            self.voice_connection = await self.connect(voiceChannel)

        newSong = None
        if str(args[0]).__contains__("list"):
            playlist = Playlist(args[0])
            for song in playlist.songs:
                self.queue.append(song)
            
            try:
                newSong = self.queue.pop(0)
            except (IndexError, ValueError, KeyError):
                return False, await self.create_embed_message(myLanguage['fails'][3], [])
        else:
            newSong = await self.youtube.getSong(args)

        # Returns newSong if it's a tuple object, because that means something in getSong() went wrong!
        if type(newSong) == tuple:
            return False, await self.create_embed_message(myLanguage['fails'][newSong[0]], newSong[1])
        
        if newSong is not None and type(newSong) == Song:
            self.queue.append(newSong)
            
        if self.voice_connection.is_playing() or self.voice_connection.is_paused():
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [newSong.song_title, newSong.viewCount]))
            return True, None

        if not self.in_queue_loop:
            await self.queue_loop()

        # Tells the main program that no error was found and the function worked just fine
        return True, None
        
    async def queue_loop(self):
        myLanguage = self.language['commands']['playing']

        self.in_queue_loop = True
        while len(self.queue) > 0:

            self.current_song = None
            self.current_progress = 0

            currentSong = self.queue.pop(0)
            if currentSong.player_link is None:
                currentSong.player_link = await self.youtube.get_player_link(currentSong.youtube_link)

            if currentSong.audio_source is None:
                await currentSong.init_audio_source()

            self.current_song = currentSong
            self.title_backup = currentSong.song_title

            # Sends special message to channel
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [currentSong.song_title, currentSong.youtube_link]))

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

        self.in_queue_loop = False
        await self.stop()
        await self.disconnect()

    async def skip(self):
        myLanguage = self.language['commands']['skip']
        title = self.current_song.song_title

        if self.voice_connection is not None and self.voice_connection.is_connected() and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
            self.skipping = True
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [title]))
            return True, None
        return False, await self.create_embed_message(myLanguage['fails'][0], [])

    async def pause(self):
        myLanguage = self.language['commands']['pause']

        if self.voice_connection is not None and self.voice_connection.is_playing():
            self.voice_connection.pause()
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [(self.current_song.song_title, self.current_progress)]))
            return True, None
        return False, await self.create_embed_message(myLanguage['fails'][0], [])

    async def resume(self):
        myLanguage = self.language['commands']['resume']

        if self.voice_connection is not None and self.voice_connection.is_paused():
            self.voice_connection.resume()
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [(self.current_song.song_title, self.current_progress)]))
            return True, None
        return False, await self.create_embed_message(myLanguage['fails'][0], [])

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
        myLanguage = self.language['commands']['stop']

        self.current_song = None
        self.current_progress = 0

        if self.voice_connection is not None and self.voice_connection.is_playing():

            # Empty the current queue
            self.queue = []

            # Stop the MediaPlayer
            self.voice_connection.stop()

            # Sends special message
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [self.title_backup]))

            # Initiate disconnect
            await self.disconnect()
        else:
            return False, await self.create_embed_message(myLanguage['fails'][0], [])
        return True, None

    async def disconnect(self, delay=120):
        if self.disconnecting:
            return

        self.disconnecting = True
        if self.voice_connection is None:
            await self.voice_connection.disconnect(force=True)

        for i in range(delay):
            if self.voice_connection is not None and (self.voice_connection.is_playing() or self.voice_connection.is_paused()):
                self.disconnecting = False
                return

            if i % 30 == 0 and i > 59:
                await self.send_user_message("Disconnecting in "+str(delay-i)+" seconds!")
            await asyncio.sleep(1)

        if self.voice_connection.is_connected() and not self.voice_connection.is_playing() and not self.voice_connection.is_paused():
            await self.voice_connection.disconnect(force=True)
            self.disconnecting = False

    async def show_current_song(self):
        myLanguage = self.language['commands']['np']

        if self.current_song is not None:
            
            cProgress = ""
            progress = int((self.current_progress / (self.current_song.duration / 100)) / 2)
            
            for i in range(50):
                if i == progress:
                    cProgress += "O"
                else:
                    cProgress += "="

            await self.send_embed(await self.create_embed_message(myLanguage['works'], [self.current_song.song_title, self.current_song.viewCount, cProgress, str(int(progress*2))+"%", str(self.current_progress)+"s / "+str(self.current_song.duration)+"s"]))
            return True, None
        else:
            return False, await self.create_embed_message(myLanguage['fails'][0], [])
    
    async def show_current_queue(self, page=1):
        myLanguage = self.language['commands']['queue']
        
        message = ""

        _max = (page * 10)
        _min = _max - 10

        if len(self.queue) > 0:
            for i in range(_min, _max):
                try:
                    song = self.queue[i]
                    message += str(i+1) + ". "+str(song.song_title) + ", Aufrufe: "+str(song.viewCount)+"\n"
                except (IndexError, KeyError):
                    break
            message += "\nDas Maximum sind 10 Songs pro Seite!"

            await self.send_embed(await self.create_embed_message(myLanguage['works'], [message]))
            return True, None
        else:
            return False, await self.create_embed_message(myLanguage['fails'][0], [])

    async def clear_current_queue(self):
        myLanguage = self.language['commands']['clear']
        self.queue = []
        return False, self.create_embed_message(myLanguage['works'], [len(self.queue)])

    async def clear_messages(self):
        myLanguage = self.language['commands']['cleaner']
        for channel in self.guild.channels:
            if channel.name == self.bound_channel and type(channel) == discord.TextChannel:
                await channel.purge(limit=100)
                await self.send_embed(await self.create_embed_message(myLanguage['works'], []))
                return True, None
        return True, None

    async def change_language(self, code):
        global languageHandler
        myLanguage = self.language['commands']['lang']

        if languageHandler.code_exists(code):
            self.language = languageHandler.get_language(code)
            old_code = self.country_code
            self.country_code = code
            await self.send_embed(await self.create_embed_message(myLanguage['works'], [(old_code, code)]))
            return True, None
        else:
            return False, await self.create_embed_message(myLanguage['fails'][0], [])


