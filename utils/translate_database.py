# Imports
import json
from time import sleep
from mysql import connector
from deep_translator import GoogleTranslator

host = "localhost"
port = 3306
user = "root"
database = "musicbot"
password = ""
connection = connector.connect(
    host=host,
    port=port,
    user=user,
    password=password,
    database=database
)


def get_german_responses() -> list:
    sql_statement = """SELECT * FROM responses WHERE language_id=0"""
    cursor = connection.cursor()
    cursor.execute(sql_statement)

    responses = []
    for row in cursor.fetchall():
        columns = []
        for column in row:
            columns.append(column)
        responses.append(columns)
    return responses


def delete_other_responses():
    sql_statement = """DELETE FROM responses WHERE language_id != 0"""
    cursor = connection.cursor()
    cursor.execute(sql_statement)
    connection.commit()


def create_json_file(langs: list):
    print("Inserting responses!")
    json_string = json.dumps(langs)
    with open("saved_responses.json", "w+", encoding="utf-8") as outfile:
        outfile.write(json_string)


def read_json_file(json_file: str) -> object:
    with open(json_file, "r", encoding="utf-8") as infile:
        json_object = json.loads(infile.read())
        return json_object
    return None


def insert_data(langs: list):
    # Get cursor
    cursor = connection.cursor()

    for language in langs:
        sql_statement = """INSERT INTO responses (id, identifier, command, color, language_id, headline, body) VALUES """
        # print("Length: " + str(len(language['responses'])))
        for i, lang in enumerate(language['responses']):
            # print("i: " + str(i))
            if i == len(language['responses']) - 1:
                sql_statement += "(%d, '%s', '%s', '%s', %d, '%s', '%s');" % (0, lang['identifier'], lang['command'], lang['color'], lang['language_id'], lang['headline'].replace("'", ""), lang['body'].replace("'", ""))
            else:
                sql_statement += "(%d, '%s', '%s', '%s', %d, '%s', '%s'), " % (0, lang['identifier'], lang['command'], lang['color'], lang['language_id'], lang['headline'].replace("'", ""), lang['body'].replace("'", ""))

        # print("My statement")
        # print(sql_statement)

        cursor.execute(sql_statement)
        connection.commit()
        print("Updated/Inserted ", cursor.rowcount, " rows.")
    print("Done!")


def translate_responses() -> list:
    found = False
    languages = []
    german_responses = get_german_responses()
    supported_languages = GoogleTranslator().get_supported_languages(as_dict=True)

    for index, key in enumerate(supported_languages, 1):
        print("\r"+str(index)+". Translating language "+str(key))
        c_code = supported_languages[key]
        if c_code != 'de':
            language = {
                'country_code': c_code,
                'full_name': key,
                'responses': []
            }

            lang_id = index
            if found:
                lang_id = index - 1

            translator = GoogleTranslator(source="de", target=c_code)
            for response in german_responses:
                print("\rTranslate nr. " + str(response[0]), end="")
                headline = None
                body = None
                while headline is None or body is None:
                    try:
                        headline = translator.translate(response[5])
                        body = translator.translate(response[6])
                    except:
                        translator = GoogleTranslator(source="de", target=c_code)
                        sleep(1)

                translated_response = {
                    'identifier': response[1],
                    'command': response[2],
                    'color': response[3],
                    'language_id': lang_id,
                    'headline': headline,
                    'body': body
                }
                language['responses'].append(translated_response)
                sleep(.125)
            languages.append(language)
        else:
            found = True
    return languages


# Delete all responses
delete_other_responses()

# Get translated responses
languages = translate_responses()

# Create json with new responses
create_json_file(languages)

# Insert data to database
insert_data(languages)
