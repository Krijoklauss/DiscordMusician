import discord
from control.model.utility.Values import LANGUAGES


def init_responses(database):
    responses = database.get_responses()
    for response in responses:
        LANGUAGES[response[4]]['responses'].append({
            'identifier': response[1],
            'command': response[2],
            'color': response[3],
            'headline': response[5],
            'body': response[6],
        })


def get_response(language_id: int, command: str, identifier: str) -> dict or None:
    for response in LANGUAGES[language_id]['responses']:
        if response['command'] == command and response['identifier'] == identifier:
            return response
    return get_default_response(language_id)


def get_default_response(language_id: int) -> dict or None:
    for response in LANGUAGES[language_id]['responses']:
        if response['command'] == "None" and response['identifier'] == "not_found":
            return response
    return None


def create_discord_response(language_id: int, command: str, identifier: str, values=()) -> discord.Embed or None:
    response = get_response(language_id, command, identifier)
    return discord.Embed(
        title=response['headline'],
        description=response['body'] % values,
        color=int(response['color'], 0)
    )


def get_language_data(language_id: int) -> dict:
    return LANGUAGES[language_id]


def language_exists(country_code: str) -> bool:
    for language in LANGUAGES:
        if language['country_code'] == country_code:
            return True
    return False


def get_language_id(country_code: str) -> int:
    for index, language in enumerate(LANGUAGES):
        if language['country_code'] == country_code:
            return index
    return 0


def get_language_name(language_id: int) -> str or None:
    try:
        return LANGUAGES[language_id]['full_name']
    except IndexError:
        pass
    return None
