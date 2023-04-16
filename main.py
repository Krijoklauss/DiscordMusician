# Imports
import sys
import discord
import logging
import control.MusicHandler as MusicHandler
from pynput import keyboard
from control.model.Command import Command
from control.DatabaseConnection import DatabaseConnection
from control.model.utility.SongFetcher import init_apis
from control.model.utility.Responses import init_responses
from control.model.utility.Responses import create_discord_response

# Disable cache
sys.dont_write_bytecode = True

# Predefined values
MOTD = "Launching Musician V2!"
HOST_TYPE = "MUSIC_BOT_SNAPSHOT"
database = DatabaseConnection()
TOKEN = database.get_token(HOST_TYPE)

# Initialize APIs
init_apis(HOST_TYPE, database)

# Init responses
init_responses(database)

# Discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)
client_name = "None"


# On ready Event
@client.event
async def on_ready():
    global database, client, client_name, MOTD

    # Set client name
    client_name = client.user.name

    # Set client status
    motd = discord.Game(MOTD)
    await client.change_presence(status=discord.Status.online, activity=motd)

    # Loading Musicians
    MusicHandler.musicians = database.get_musicians(client.user.name)

    # Init nicknames for all bots
    for musician in MusicHandler.musicians:
        guild = client.get_guild(int(musician.guild_id))
        await musician.set_nick(guild, musician.nickname, "")
    print("Bot is ready!")


@client.event
async def on_message(message: discord.message):
    global database, client_name

    # Common values
    guild = message.guild
    guild_id = guild.id
    guild_name = guild.name
    author = message.author.name
    channel = message.channel

    if author == client_name:
        return

    # Get musician for the guild
    musician = MusicHandler.get_musician(guild_id)

    if musician is None:
        database.create_musician(guild_id, guild_name, "Musician V2 ~ !prefix", "!", "", 0)
        musician = MusicHandler.create_musician(guild_id, guild_name, client_name)
        # Init new nickname for new musician
        await musician.set_nick(guild, [musician.nickname], "")

    # Create new command
    command = Command(musician, message)

    # Execute command and get response
    if musician.bound_channel == "" and command.command != "bind":
        await message.delete()
        response = create_discord_response(musician.language_id, "None", "no_channel_bound")
    elif musician.bound_channel == "" and command.command == "bind":
        response = await command.execute()
    elif musician.bound_channel != message.channel.name:
        response = create_discord_response(musician.language_id, "None", "wrong_channel")
    else:
        response = await command.execute()

    # Print response from command
    if response is None:
        return
    elif type(response) == discord.Embed:
        await channel.send(embed=response)
    else:
        await channel.send(response)

    # Disconnect if required
    await musician.init_disconnect(guild)


def on_press(key):
    if key == keyboard.Key.esc:
        print("Saving values...")
        # _close()


def _close():
    # Store musician values
    database.save_musicians(MusicHandler.musicians)
    # Close program
    quit()


# Main running loop
def _run():
    global TOKEN

    try:
        print("Initializing Bot...")

        # Create Keyboard listener
        listener = keyboard.Listener(on_press=on_press)
        listener.start()

        # Run discord client
        client.run(TOKEN, log_level=logging.WARN)
    except:
        print("Fatal Error!")
        print("Stopping Musician...")
        _close()


# Check filename
if __name__ == '__main__':
    _run()
