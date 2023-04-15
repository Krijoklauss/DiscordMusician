from control.Musician import Musician

musicians = []


def create_musician(guild_id: int, server_name: str, client_name: str) -> Musician:
    # Create database row for musician
    new_musician = Musician(guild_id, server_name, client_name)
    musicians.append(new_musician)
    return new_musician


def get_musician(guild_id: int) -> Musician or None:
    for musician in musicians:
        if str(musician.guild_id) == str(guild_id):
            return musician
    return None
