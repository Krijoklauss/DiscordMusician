import discord
from control.Musician import Musician
from control.model.utility.Values import COMMANDS
from control.model.utility.Responses import create_discord_response


class Command:
    def __init__(self, musician: Musician, command: discord.message) -> None:
        self.error = create_discord_response(musician.language_id, "None", "command_not_found", values=(str(command.content)))
        self.command = ""
        self.function = ""
        self.parameter = []
        self.musician = musician
        self.guild = command.guild
        self.username = command.author.name
        self.text_channel = command.channel.name
        self.content = command.content
        self.correct_syntax = self.create_command()

    def create_command(self) -> bool:
        if self.content.startswith(self.musician.prefix):
            splitter = self.content.split(" ")
            command = splitter[0].replace(self.musician.prefix, "")
            for COMMAND in COMMANDS:
                if COMMAND['name'] == str(command):
                    self.error = None
                    self.command = command
                    self.function = COMMAND['function']
                    del splitter[0]
                    if COMMAND['parameters']:
                        if len(splitter) >= COMMAND['min']:
                            if len(splitter) <= COMMAND['max']:
                                self.parameter = splitter
                            else:
                                self.error = create_discord_response(self.musician.language_id, "None", "wrong_parameter_length", values=(COMMAND['max']))
                        else:
                            self.error = create_discord_response(self.musician.language_id, "None", "missing_parameter", values=(COMMAND['min']))
                    return True
        else:
            self.error = create_discord_response(self.musician.language_id, "None", "wrong_prefix", values=(self.content[0]))
        return False

    async def execute(self) -> str:
        # Executing function from musician
        if self.error is None:
            executor = getattr(self.musician, self.function)
            return await executor(self.guild, self.parameter, self.username)
        else:
            return self.error
            
