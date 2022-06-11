import discord
import asyncio
from datetime import datetime

from control.model.utility import PHUtility as ph
from control.GuildHandler import GuildHandler



# This class handles incoming commands from different guilds
class CommandHandler:
    def __init__(self, client_name):
        self.guildHandler = GuildHandler(client_name)
        self.phandler = ph.PHHandler()

    # Counts message send in the bind channel
    async def countUp(self, guild):
        musicBot = self.guildHandler.get_MusicBot(guild.id)
        musicBot.msg_counter = musicBot.msg_counter + 1

        if musicBot.msg_counter >= 100:
            musicBot.msg_counter = 0
            await musicBot.clear_messages()

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

    # Main Function from this class which handles the incoming messages
    async def handle(self, msg: discord.message):
        # Declaring variables
        guild = msg.guild
        content = msg.content
        channel = msg.channel.name
        musicBot = self.guildHandler.get_MusicBot(guild.id)
        musicBot.guild = guild

        # Sets the current language of the Bot to respond in the correct lang
        language = musicBot.language

        # The first thing we check is the last command that has been executed!
        difference = 999999
        lastCommand = self.guildHandler.get_Last_Command_Time(guild.id)
        if lastCommand is not None:
            cTime = datetime.now()
            difference = (cTime - lastCommand).total_seconds()

        # Updates the last command executed timer
        self.guildHandler.set_Last_Command_Time(guild.id)
        
        # Checking for correct channel
        if musicBot.is_bound:
            if channel != musicBot.bound_channel:
                return
        
        # Checking for correct prefix
        prefix = ""
        try:
            prefix = content[0]
        except IndexError:
            pass

        if musicBot.prefix != prefix:
            return

        args = []
        splitter = content.split(" ")
        command = splitter[0].replace(prefix, "")
        
        try:
            # Testing if arguments are provided
            args = splitter[1:len(splitter)]
        except IndexError:
            print("No arguments provided!")


        # Getting my current language to send valid bot messages
        myLanguage = musicBot.language['commands']['basicerrors']['fails']

        # Checking if too many arguments are provided!
        argsExceptions = ["nick", "play"]
        if len(args) > 1 and not argsExceptions.__contains__(command):
            await msg.channel.send(embed=await self.create_embed_message(myLanguage[0], []))
            return

        # Check if command needs an argument!
        needsArguments = ["prefix", "bind", "nick", "play", "seek", "lang", "percentage"]
        if len(args) < 1 and needsArguments.__contains__(command):
            await msg.channel.send(embed=await self.create_embed_message(myLanguage[1], []))
            return

        if not musicBot.is_bound and command != "bind":
            await msg.channel.send(embed=await self.create_embed_message(myLanguage[2], []))
            return

        # Executes the required function!
        if command == "prefix":
            status, responseMessage = await musicBot.set_prefix(args[0])      
        elif command == "bind":
            status, responseMessage = await musicBot.set_bind(guild, args[0])
        elif command == "nick":
            status, responseMessage = await musicBot.set_nick(guild, args)
        elif command == "play":
            # Sleeps the thread for a specific time, depends on the execution timeout (This sleep timer is important to stop simultanious execution of the play function!)
            if difference <= 0.5:
                await asyncio.sleep(0.5)
            status, responseMessage = await musicBot.play(guild, msg.author.name, args)
        elif command == "stop":
            status, responseMessage = await musicBot.stop()
        elif command == "skip":
            status, responseMessage = await musicBot.skip()
        elif command == "pause":
            status, responseMessage = await musicBot.pause()
        elif command == "resume":
            status, responseMessage = await musicBot.resume()
        elif command == "seek":
            status, responseMessage = await musicBot.seek(args[0])
        elif command == "np":
            status, responseMessage = await musicBot.show_current_song()
        elif command == "queue":
            if len(args) > 0:
                try:
                    p = int(args[0])
                    status, responseMessage = await musicBot.show_current_queue(page=p)
                except:
                    return 
            else:
                status, responseMessage = await musicBot.show_current_queue()
        elif command == "clear":
            status, responseMessage = await musicBot.clear_current_queue()
        elif command == "cleaner":
            status, responseMessage = await musicBot.clear_messages()
        elif command == "help":
            status, responseMessage = await musicBot.show_help_message()
        elif command == "lang":
            status, responseMessage = await musicBot.change_language(args[0])
        elif command == "languages":
            status, responseMessage = await musicBot.show_languages()
        elif command == "teams":
            status, responseMessage = await self.phandler.build_teams(msg)
        elif command == "percentage":
            status, responseMessage = await self.phandler.set_percent(int(args[0]))
        else:
            await msg.channel.send("Der Command den Sie eingegeben haben existiert nicht! ("+str(command)+")")
            return

        # Sends error message on False status!
        if not status:
            await msg.channel.send(embed=responseMessage)

