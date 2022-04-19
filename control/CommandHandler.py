import asyncio
import discord
from datetime import datetime
from control.GuildHandler import GuildHandler



class CommandHandler:
    def __init__(self):
        self.guildHandler = GuildHandler()

    async def countUp(self, guild):
        print("Counting up!")
        musicBot = self.guildHandler.get_MusicBot(guild.id)
        musicBot.msg_counter = musicBot.msg_counter + 1

        print("Msgs: "+str(musicBot.msg_counter))

        if musicBot.msg_counter >= 100:
            musicBot.msg_counter = 0
            await musicBot.clear_messages()

    async def handle(self, msg: discord.message):
        # Declaring variables
        guild = msg.guild
        content = msg.content
        channel = msg.channel.name
        musicBot = self.guildHandler.get_MusicBot(guild.id)
        musicBot.guild = guild

        # The first thing we check is the last command that has been executed!
        difference = 999999
        lastCommand = self.guildHandler.get_Last_Command_Time(guild.id)
        if lastCommand is not None:
            cTime = datetime.now()
            difference = (cTime - lastCommand).total_seconds()

        # Updates the last command executed timer
        self.guildHandler.set_Last_Command_Time(guild.id)
        
        # Shows difference of time in console
        print("Difference between last commands is: "+str(difference))
        
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
            await msg.channel.send("Falscher prefix!\nIhr prefix lautet: "+str(musicBot.prefix))
            return

        args = []
        splitter = content.split(" ")
        command = splitter[0].replace(prefix, "")
        
        try:
            # Testing if arguments are provided
            args = splitter[1:len(splitter)]
        except IndexError:
            print("No arguments provided!")

        # Checking if too many arguments are provided!
        argsExceptions = ["nick", "play"]
        if len(args) > 1 and not argsExceptions.__contains__(command):
            await msg.channel.send("Sie dürfen nur maximal ein einziges Argument angeben!")
            return

        if not musicBot.is_bound and command != "bind":
            await msg.channel.send("Sie müssen den Bot zuerst mit dem Befehl '!bind' einem Channel zuordnen!")
            return

        # Sets new prefix for your guild
        if command == "prefix":
            status, responseMessage = await musicBot.set_prefix(args[0])      
        elif command == "bind":
            status, responseMessage = await musicBot.set_bind(guild, args[0])
        elif command == "nick":
            status, responseMessage = await musicBot.set_nick(guild, args)
        elif command == "play":

            # Sleeps the thread for a specific time, depends on the execution timeout
            if difference <= 1.5:
                await asyncio.sleep(1)

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
            status, responseMessage = await musicBot.show_current_queue()
        elif command == "clear":
            status, responseMessage = await musicBot.clear_current_queue()
        elif command == "cleaner":
            status, responseMessage = await musicBot.clear_messages()
        elif command == "help":
            status, responseMessage = await musicBot.show_help_message()
        else:
            await msg.channel.send("Der Command den Sie eingegeben haben existiert nich! ("+str(command)+")")
            return

        # Sends error message on False status!
        if not status:
            await msg.channel.send(responseMessage)

