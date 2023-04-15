from mysql import connector

# Init connection
connection = connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="musicbot"
)

new_languages = []
data = [
    # Basic errors
    ["no_channel_bound", "None", "140,0,0", "Fehler", "Bitte verknüpfen Sie zuerst einen Textkanal!"],
    ["wrong_channel", "None", "140,0,0", "Fehler", "Bitte schreiben Sie nur in ihrem verknüpften Textkanal!"],
    ["missing_parameter", "None", "140,0,0", "Fehler", "Dieser Command benötigt mindestens %s parameter"],
    ["no_parameter_required", "None", "140,0,0", "Fehler", "Dieser Command benötigt keine parameter!"],
    ["wrong_parameter_length", "None", "140,0,0", "Fehler", "Dieser Command hat eine maximale Parameterlänge von %s"],
    ["not_found", "None", "140,0,0", "Fehler", "Ein unbekannter Fehler ist aufgetreten!"],
    ["wrong_prefix", "None", "140,0,0", "Fehler", "Der Prefix %s ist falsch!"],
    ["command_not_found", "None", "140,0,0", "Fehler", "Der Command %s existiert nicht!"],

    # Execution errors
    ["channel_not_found", "bind", "140,0,0", "Fehler", "Der Textkanal %s wurde nicht gefunden!"],
    ["prefix_not_allowed", "prefix", "140,0,0", "Fehler", "Der neue prefix %s ist nicht erlaubt"],
    ["nickname_too_long", "nick", "140,0,0", "Fehler", "Der nickname %s ist zu lang!"],
    ["nickname_too_many_words", "nick", "140,0,0", "Fehler", "Der neue nickname hat zu viele Wörter!"],
    ["bot_not_found", "nick", "140,0,0", "Fehler", "Der Musikbot wurde nicht gefunden?!"],
    ["queue_creation_failed", "play", "140,0,0", "Fehler", "Es konnte keine queue aus den angegebenen Parametern erstellt werden!"],
    ["bot_not_connected", "play", "140,0,0", "Fehler", "Der Bot ist nicht mit einem Sprachkanl verbunden!"],
    ["audio_source_failed", "play", "140,0,0", "Fehler", "Es konnte keine Audio Resource erstellt werden! Bitte wiederholen Sie die Eingabe!"],
    ["skip_failed", "skip", "140,0,0", "Fehler", "Es gibt keinen Song der übersprungen werden kann!"],
    ["resume_failed", "resume", "140,0,0", "Fehler", "Es wurde kein Song pausiert!"],
    ["pause_failed", "pause", "140,0,0", "Fehler", "Es gibt keinen Song der pausiert werden könnte!"],
    ["stop_failed", "stop", "140,0,0", "Fehler", "Es wird gerade kein Song abgespielt!"],
    ["loop_failed", "loop", "140,0,0", "Fehler", "Es kann nicht sowohl queue loop als auch song loop aktiviert sein!"],
    ["loopqueue_failed", "loopqueue", "140,0,0", "Fehler", "Es kann nicht sowohl Song loop als auch Queue loop aktiviert sein!"],
    ["queue_empty", "queue", "140,0,0", "Fehler", "Es gibt aktuell keine Warteschlange!"],
    ["queue_page_not_exists", "queue", "140,0,0", "Fehler", "Die Warteschlange hat keine Seite %s!"],
    ["say_failed_music", "say", "140,0,0", "Fehler", "Es darf währenddessen keine Musik abgespielt werden!"],
    ["say_failed_parameter", "say", "140,0,0", "Fehler", "Die Parameter die Sie angegeben haben sind Fehlerhaft!"],
    ["say_failed_mp3", "say", "140,0,0", "Fehler", "Es konnte keine MP3 Datei erstellt werden!"],
    ["show_current_song_failed", "show_current_song", "140,0,0", "Fehler", "Es wird keine Musik abgespielt!"],
    ["clean_channel_failed", "cleaner", "140,0,0", "Erfolg", "Der Textkanal wurde nicht gefunden!"],
    ["language_failed", "language", "140,0,0", "Fehler", "Diese Sprache existiert nicht!"],

    # Execution success
    ["bind_success", "bind", "30,201,0", "Erfolg", "Der neue Channel für %s lautet nun %s!"],
    ["prefix_success", "prefix", "30,201,0", "Erfolg", "Der neue prefix lautet nun %s!"],
    ["nick_success", "nick", "30,201,0", "Erfolg", "Der neue nickname lautet nun %s!"],
    ["now_playing", "play", "30,201,0", "Erfolg", "Der Song %s wird jetzt abgespielt!"],
    ["empty_queue", "play", "30,201,0", "Erfolg", "Die Warteschlange hat keine Songs mehr zum abspielen!"],
    ["added_song", "play", "30,201,0", "Erfolg", "Der Song %s wurde zur Warteschlange hinzugefügt!"],
    ["skip_success", "skip", "30,201,0", "Erfolg", "Der Song %s wurde übersprungen!"],
    ["resume_success", "resume", "30,201,0", "Erfolg", "Der Song %s wird nun weiter abgespielt!"],
    ["pause_success", "pause", "30,201,0", "Erfolg", "Der Song %s wurde pausiert!"],
    ["stop_success", "stop", "30,201,0", "Erfolg", "Das Abspielen von Musik wurde unterbunden!"],
    ["loop_passive", "loop", "30,201,0", "Erfolg", "Der Song loop wurde nun deaktiviert!"],
    ["loop_active", "loop", "30,201,0", "Erfolg", "Der Song loop wurde nun aktiviert!"],
    ["loopqueue_passive", "loopqueue", "30,201,0", "Erfolg", "Der Queue loop wurde nun deaktiviert!"],
    ["loopqueue_active", "loopqueue", "30,201,0", "Erfolg", "Der Queue loop wurde nun aktiviert!"],
    ["queue_success", "queue", "30,201,0", "Erfolg", "Die Warteschlange auf Seite %s sieht wie folgt aus: \n %s"],
    ["clear_success", "clear", "30,201,0", "Erfolg", "Die queue wurde geleert!"],
    ["say_success", "say", "30,201,0", "Erfolg", "%s"],
    ["show_current_song_success", "show_current_song", "30,201,0", "Erfolg", "Youtube: %s\nName: %s\nChannel: %s\nAufrufe: %s\n%s\nUploaded: %s"],
    ["clean_channel_success", "cleaner", "30,201,0", "Erfolg", "Es wurden 100 Nachrichten gelöscht!"],
    ["help_success", "help", "30,201,0", "Erfolg", "Der Bot akzeptiert folgende Befehle:\n\n%s"],
    ["languages_success", "languages", "30,201,0", "Erfolg", "Der Bot akzeptiert folgende Sprachen:\n\n%s"],
    ["language_success", "language", "30,201,0", "Erfolg", "Die neue Sprache ist jetzt %s!"]
]


def rgb_to_hex(rgb):
    return '0x%02x%02x%02x' % rgb


for lang in data:
    color_splitter = lang[2].split(',')
    color_tuple = (int(color_splitter[0]), int(color_splitter[1]), int(color_splitter[2]))

    new_languages.append({
        'identifier': lang[0],
        'command': lang[1],
        'color': rgb_to_hex(color_tuple),
        'language_id': 0,
        'headline': lang[3],
        'body': lang[4],
    })


def delete_values():
    cursor = connection.cursor()
    sql_statement = "DELETE FROM responses"
    cursor.execute(sql_statement)
    connection.commit()
    print(cursor.rowcount, "record(s) deleted")


def update_auto_increment():
    sql_statement = """ALTER TABLE responses AUTO_INCREMENT = 1"""
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    connection.commit()
    print("Updated auto increment value!")


def insert_values():
    # Creating mysql sql_statement
    sql_statement = """INSERT INTO responses (id, identifier, command, color, language_id, headline, body) VALUES """
    for i, new_language in enumerate(new_languages):
        if i == len(new_languages) - 1:
            sql_statement += "(%d, '%s', '%s', '%s', %d, '%s', '%s');" % (0, new_language['identifier'], new_language['command'], new_language['color'], new_language['language_id'], new_language['headline'], new_language['body'])
        else:
            sql_statement += "(%d, '%s', '%s', '%s', %d, '%s', '%s'), " % (0, new_language['identifier'], new_language['command'], new_language['color'], new_language['language_id'], new_language['headline'], new_language['body'])

    # Send data
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    connection.commit()
    print("Updated/Inserted ", cursor.rowcount, " rows.")


# Deleting current responses
delete_values()

# Resets Auto increment value
update_auto_increment()

# Insert new responses
insert_values()
