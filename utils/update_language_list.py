import json
from deep_translator import GoogleTranslator

supported = GoogleTranslator().get_supported_languages(as_dict=True)
languages = []
for key in supported:
    country_code = supported[key]
    languages.append({
        'country_code': country_code,
        'full_name': str(key).capitalize(),
        'responses': []
    })

with open("languages.json", "w+", encoding="utf-8") as outfile:
    json_string = json.dumps(languages, indent=4)
    outfile.write(json_string)
