import math
import random
import discord
from pandas import array


class PHHandler():

    def __init__(self) -> None:
        self.cop_percentage = 30
        pass

    async def set_percent(self, p):
        self.cop_percentage = p
        return True, []

    # Gets a random number between x and y
    async def get_random_number(self, _min, _max):
        return random.randint(_min, _max)

    # Shuffel array
    async def shuffle_array(self, array):
        for i in range((len(array)-1) * 2):
            j = math.ceil((i / 2))

            elem = array[j]
            temp = elem

            newPosition = await self.get_random_number(0, len(array)-1)
            array[j] = array[newPosition]
            array[newPosition] = temp

    # Builds PH Teams
    async def build_teams(self, msg: discord.Message):

        guild = msg.guild
        author = msg.author
        channel = author.voice.channel

        # Checking if the user is connected to a channel
        if channel is None:
            return True, []
        
        lobby = []
        for member in channel.members:
            lobby.append(member)

        if len(lobby) < 3:
            return True, []

        # Init final values
        cops = []
        robbers = []
        _maxcops = round((len(lobby) / 100) * self.cop_percentage)
        await self.shuffle_array(lobby)
        
        # Place cops and robbers in correct groups
        for i in range(_maxcops):
            c = lobby.pop(i)
            cops.append(c)

        for r in lobby:
            robbers.append(r)

        cop_mover = None
        for c in guild.channels:
            if type(c) == discord.channel.VoiceChannel:
                if c.name == channel.name:
                    pass
                else:
                    cop_mover = c
                    break
        
        if cop_mover is None:
            return True, []
        
        for c in cops:
            await c.move_to(cop_mover)

        return True, []

