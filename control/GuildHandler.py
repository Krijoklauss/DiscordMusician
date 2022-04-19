import json
from datetime import datetime
from control.MediaPlayer import MediaPlayer

class GuildHandler:
    def __init__(self):
        self.guilds = {}
        self.loadGuilds()
        pass

    def loadGuilds(self):
        print("Loading available guilds!")
        try:
            _j = {}
            with open("data/guilds.json", "r", encoding="UTF-8") as infile:
                _j = json.loads(infile.read())
                infile.flush()
                infile.close()

            for id in _j:
                player = MediaPlayer(id, pref=_j[id]['prefix'], bounded=_j[id]['channel_bound'], chan=_j[id]['bound_channel'])
                self.guilds[id] = {
                    "player": player,
                    "last_command_time": None
                }

        except FileNotFoundError:
            print("This file does not exist!")
            print("Creating new File!")
            open("data/guilds.json", "w+", encoding="UTF-8").close()

    def is_available(self, id: str):
        try:
            placeholder = self.guilds[str(id)]
            return True
        except KeyError:
            return False

    def get_MusicBot(self, id: str):
        if self.is_available(id):
            return self.guilds[str(id)]["player"]
        else:
            return self.create_bot(id)

    def get_Last_Command_Time(self, id: str):
        if self.is_available(id):
            return self.guilds[str(id)]["last_command_time"]
        else:
            return self.create_bot(str(id), time=True)

    def set_Last_Command_Time(self, id: str):
        self.guilds[str(id)]["last_command_time"] = datetime.now()
        
    def create_bot(self, identity, time=False):
        print("Id: "+str(identity))

        player = MediaPlayer(identity)
        self.guilds[str(identity)] = {
            "player": player,
            "last_command_time": None
        }
        
        if not time:
            return self.guilds[str(identity)]["player"]
        else:
            return self.guilds[str(identity)]["last_command_time"]

    def saveGuilds(self):
        print("Saving guilds!")

        obj = {}
        for id in self.guilds:
            obj[id] = {
                "prefix": self.guilds[id]["player"].prefix,
                "channel_bound": self.guilds[id]["player"].is_bound,
                "bound_channel": self.guilds[id]["player"].bound_channel
            }

        with open("data/guilds.json", "w+", encoding="UTF-8") as outfile:
            json.dump(obj, outfile, indent=4)
            outfile.flush()
            outfile.close()