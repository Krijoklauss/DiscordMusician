# Imports
from click import command
import discord
from os import environ
from control.CommandHandler import CommandHandler

# Declaring required Intents
inten = discord.Intents.default()
inten.members = True

# Declaring Bot token and initiating new discord.Client()
token = environ.get("MUSIC_BOT_SNAPSHOT")
client = discord.Client(intents=inten)

commandHandler = None
client_name = None

# Event which is called after the bot is ready for production
@client.event
async def on_ready():
    global client, client_name, commandHandler

    # Local output for dev to see if the Bot is ready! (No need to spam all guild channels on every restart!)
    print("Bot is ready!")

    # Init values with None
    client_name = client.user.name

    # Init new CommandHandler class
    commandHandler = CommandHandler(client_name)

    for guild in client.guilds:
        for channel in guild.channels:
            if type(channel) == discord.TextChannel:
                # await channel.send("Ich bin wieder online :-)")
                break

# Event which is called on every message sent in a text channel
@client.event
async def on_message(message: discord.message):
    global commandHandler

    sender = message.author
    # Goes through if type == discord.Member
    if type(sender) == discord.Member:
        
        # Counts messages send
        await commandHandler.countUp(message.guild)

        # Goes through if message wasnt sent by a bot
        if not client_name == str(message.author.name):
            # Handles incoming commands
            await commandHandler.handle(message)

# Run the Client and create new MusicBot instance
def __main__():
    global commandHandler

    # Run the Client and except on KeyboardInterrupt
    try:
        client.run(token)
    except (KeyboardInterrupt, RuntimeError):
        pass

    print("Saving current guild settings!")
    commandHandler.guildHandler.saveGuilds()


# Run main Function
__main__()
