
PREFIXES = [
    "!", "?", "-", ",", ".", "'", "/", "\\"
]

COMMANDS = [
    {'name': 'prefix',      'function': 'set_prefix',           'parameters': True,  'min': 1, 'max': 1},
    {'name': 'nick',        'function': 'set_nick',             'parameters': True,  'min': 1, 'max': 10},
    {'name': 'bind',        'function': 'set_bind',             'parameters': True,  'min': 1, 'max': 1},
    {'name': 'play',        'function': 'play',                 'parameters': True,  'min': 1, 'max': 30},
    {'name': 'p',           'function': 'play',                 'parameters': True,  'min': 1, 'max': 30},
    {'name': 'skip',        'function': 'skip',                 'parameters': False, 'min': 0, 'max': 0},
    {'name': 'pause',       'function': 'pause',                'parameters': False, 'min': 0, 'max': 0},
    {'name': 'stop',        'function': 'stop',                 'parameters': False, 'min': 0, 'max': 0},
    {'name': 'resume',      'function': 'resume',               'parameters': False, 'min': 0, 'max': 0},
    {'name': 'loop',        'function': 'loop',                 'parameters': False, 'min': 0, 'max': 0},
    {'name': 'loopqueue',   'function': 'loopqueue',            'parameters': False, 'min': 0, 'max': 0},
    {'name': 'qloop',       'function': 'loopqueue',            'parameters': False, 'min': 0, 'max': 0},
    {'name': 'ql',          'function': 'loopqueue',            'parameters': False, 'min': 0, 'max': 0},
    {'name': 'queue',       'function': 'show_queue',           'parameters': True, 'min': 0, 'max': 1},
    {'name': 'q',           'function': 'show_queue',           'parameters': True, 'min': 0, 'max': 1},
    {'name': 'seek',        'function': 'seek',                 'parameters': True,  'min': 1, 'max': 1},
    {'name': 'clear',       'function': 'clear',                'parameters': False, 'min': 0, 'max': 0},
    {'name': 'say',         'function': 'say',                  'parameters': True,  'min': 1, 'max': 3},
    {'name': 'cleaner',     'function': 'clean_channel',        'parameters': False, 'min': 0, 'max': 0},
    {'name': 'help',        'function': 'show_help',            'parameters': False, 'min': 1, 'max': 1},
    {'name': 'lang',        'function': 'set_language',         'parameters': True,  'min': 1, 'max': 1},
    {'name': 'language',    'function': 'set_language',         'parameters': True,  'min': 1, 'max': 1},
    {'name': 'languages',   'function': 'show_languages',       'parameters': False, 'min': 1, 'max': 1},
    {'name': 'cplaying',    'function': 'show_current_song',    'parameters': False, 'min': 0, 'max': 0},
    {'name': 'cp',          'function': 'show_current_song',    'parameters': False, 'min': 0, 'max': 0}
]

LANGUAGES = [
    {
        'country_code': 'de',
        'full_name': 'Deutsch',
        'responses': []
    },
    {
        "country_code": "af",
        "full_name": "Afrikaans",
        "responses": []
    },
    {
        "country_code": "sq",
        "full_name": "Albanian",
        "responses": []
    },
    {
        "country_code": "am",
        "full_name": "Amharic",
        "responses": []
    },
    {
        "country_code": "ar",
        "full_name": "Arabic",
        "responses": []
    },
    {
        "country_code": "hy",
        "full_name": "Armenian",
        "responses": []
    },
    {
        "country_code": "as",
        "full_name": "Assamese",
        "responses": []
    },
    {
        "country_code": "ay",
        "full_name": "Aymara",
        "responses": []
    },
    {
        "country_code": "az",
        "full_name": "Azerbaijani",
        "responses": []
    },
    {
        "country_code": "bm",
        "full_name": "Bambara",
        "responses": []
    },
    {
        "country_code": "eu",
        "full_name": "Basque",
        "responses": []
    },
    {
        "country_code": "be",
        "full_name": "Belarusian",
        "responses": []
    },
    {
        "country_code": "bn",
        "full_name": "Bengali",
        "responses": []
    },
    {
        "country_code": "bho",
        "full_name": "Bhojpuri",
        "responses": []
    },
    {
        "country_code": "bs",
        "full_name": "Bosnian",
        "responses": []
    },
    {
        "country_code": "bg",
        "full_name": "Bulgarian",
        "responses": []
    },
    {
        "country_code": "ca",
        "full_name": "Catalan",
        "responses": []
    },
    {
        "country_code": "ceb",
        "full_name": "Cebuano",
        "responses": []
    },
    {
        "country_code": "ny",
        "full_name": "Chichewa",
        "responses": []
    },
    {
        "country_code": "zh-CN",
        "full_name": "Chinese (simplified)",
        "responses": []
    },
    {
        "country_code": "zh-TW",
        "full_name": "Chinese (traditional)",
        "responses": []
    },
    {
        "country_code": "co",
        "full_name": "Corsican",
        "responses": []
    },
    {
        "country_code": "hr",
        "full_name": "Croatian",
        "responses": []
    },
    {
        "country_code": "cs",
        "full_name": "Czech",
        "responses": []
    },
    {
        "country_code": "da",
        "full_name": "Danish",
        "responses": []
    },
    {
        "country_code": "dv",
        "full_name": "Dhivehi",
        "responses": []
    },
    {
        "country_code": "doi",
        "full_name": "Dogri",
        "responses": []
    },
    {
        "country_code": "nl",
        "full_name": "Dutch",
        "responses": []
    },
    {
        "country_code": "en",
        "full_name": "English",
        "responses": []
    },
    {
        "country_code": "eo",
        "full_name": "Esperanto",
        "responses": []
    },
    {
        "country_code": "et",
        "full_name": "Estonian",
        "responses": []
    },
    {
        "country_code": "ee",
        "full_name": "Ewe",
        "responses": []
    },
    {
        "country_code": "tl",
        "full_name": "Filipino",
        "responses": []
    },
    {
        "country_code": "fi",
        "full_name": "Finnish",
        "responses": []
    },
    {
        "country_code": "fr",
        "full_name": "French",
        "responses": []
    },
    {
        "country_code": "fy",
        "full_name": "Frisian",
        "responses": []
    },
    {
        "country_code": "gl",
        "full_name": "Galician",
        "responses": []
    },
    {
        "country_code": "ka",
        "full_name": "Georgian",
        "responses": []
    },
    {
        "country_code": "el",
        "full_name": "Greek",
        "responses": []
    },
    {
        "country_code": "gn",
        "full_name": "Guarani",
        "responses": []
    },
    {
        "country_code": "gu",
        "full_name": "Gujarati",
        "responses": []
    },
    {
        "country_code": "ht",
        "full_name": "Haitian creole",
        "responses": []
    },
    {
        "country_code": "ha",
        "full_name": "Hausa",
        "responses": []
    },
    {
        "country_code": "haw",
        "full_name": "Hawaiian",
        "responses": []
    },
    {
        "country_code": "iw",
        "full_name": "Hebrew",
        "responses": []
    },
    {
        "country_code": "hi",
        "full_name": "Hindi",
        "responses": []
    },
    {
        "country_code": "hmn",
        "full_name": "Hmong",
        "responses": []
    },
    {
        "country_code": "hu",
        "full_name": "Hungarian",
        "responses": []
    },
    {
        "country_code": "is",
        "full_name": "Icelandic",
        "responses": []
    },
    {
        "country_code": "ig",
        "full_name": "Igbo",
        "responses": []
    },
    {
        "country_code": "ilo",
        "full_name": "Ilocano",
        "responses": []
    },
    {
        "country_code": "id",
        "full_name": "Indonesian",
        "responses": []
    },
    {
        "country_code": "ga",
        "full_name": "Irish",
        "responses": []
    },
    {
        "country_code": "it",
        "full_name": "Italian",
        "responses": []
    },
    {
        "country_code": "ja",
        "full_name": "Japanese",
        "responses": []
    },
    {
        "country_code": "jw",
        "full_name": "Javanese",
        "responses": []
    },
    {
        "country_code": "kn",
        "full_name": "Kannada",
        "responses": []
    },
    {
        "country_code": "kk",
        "full_name": "Kazakh",
        "responses": []
    },
    {
        "country_code": "km",
        "full_name": "Khmer",
        "responses": []
    },
    {
        "country_code": "rw",
        "full_name": "Kinyarwanda",
        "responses": []
    },
    {
        "country_code": "gom",
        "full_name": "Konkani",
        "responses": []
    },
    {
        "country_code": "ko",
        "full_name": "Korean",
        "responses": []
    },
    {
        "country_code": "kri",
        "full_name": "Krio",
        "responses": []
    },
    {
        "country_code": "ku",
        "full_name": "Kurdish (kurmanji)",
        "responses": []
    },
    {
        "country_code": "ckb",
        "full_name": "Kurdish (sorani)",
        "responses": []
    },
    {
        "country_code": "ky",
        "full_name": "Kyrgyz",
        "responses": []
    },
    {
        "country_code": "lo",
        "full_name": "Lao",
        "responses": []
    },
    {
        "country_code": "la",
        "full_name": "Latin",
        "responses": []
    },
    {
        "country_code": "lv",
        "full_name": "Latvian",
        "responses": []
    },
    {
        "country_code": "ln",
        "full_name": "Lingala",
        "responses": []
    },
    {
        "country_code": "lt",
        "full_name": "Lithuanian",
        "responses": []
    },
    {
        "country_code": "lg",
        "full_name": "Luganda",
        "responses": []
    },
    {
        "country_code": "lb",
        "full_name": "Luxembourgish",
        "responses": []
    },
    {
        "country_code": "mk",
        "full_name": "Macedonian",
        "responses": []
    },
    {
        "country_code": "mai",
        "full_name": "Maithili",
        "responses": []
    },
    {
        "country_code": "mg",
        "full_name": "Malagasy",
        "responses": []
    },
    {
        "country_code": "ms",
        "full_name": "Malay",
        "responses": []
    },
    {
        "country_code": "ml",
        "full_name": "Malayalam",
        "responses": []
    },
    {
        "country_code": "mt",
        "full_name": "Maltese",
        "responses": []
    },
    {
        "country_code": "mi",
        "full_name": "Maori",
        "responses": []
    },
    {
        "country_code": "mr",
        "full_name": "Marathi",
        "responses": []
    },
    {
        "country_code": "mni-Mtei",
        "full_name": "Meiteilon (manipuri)",
        "responses": []
    },
    {
        "country_code": "lus",
        "full_name": "Mizo",
        "responses": []
    },
    {
        "country_code": "mn",
        "full_name": "Mongolian",
        "responses": []
    },
    {
        "country_code": "my",
        "full_name": "Myanmar",
        "responses": []
    },
    {
        "country_code": "ne",
        "full_name": "Nepali",
        "responses": []
    },
    {
        "country_code": "no",
        "full_name": "Norwegian",
        "responses": []
    },
    {
        "country_code": "or",
        "full_name": "Odia (oriya)",
        "responses": []
    },
    {
        "country_code": "om",
        "full_name": "Oromo",
        "responses": []
    },
    {
        "country_code": "ps",
        "full_name": "Pashto",
        "responses": []
    },
    {
        "country_code": "fa",
        "full_name": "Persian",
        "responses": []
    },
    {
        "country_code": "pl",
        "full_name": "Polish",
        "responses": []
    },
    {
        "country_code": "pt",
        "full_name": "Portuguese",
        "responses": []
    },
    {
        "country_code": "pa",
        "full_name": "Punjabi",
        "responses": []
    },
    {
        "country_code": "qu",
        "full_name": "Quechua",
        "responses": []
    },
    {
        "country_code": "ro",
        "full_name": "Romanian",
        "responses": []
    },
    {
        "country_code": "ru",
        "full_name": "Russian",
        "responses": []
    },
    {
        "country_code": "sm",
        "full_name": "Samoan",
        "responses": []
    },
    {
        "country_code": "sa",
        "full_name": "Sanskrit",
        "responses": []
    },
    {
        "country_code": "gd",
        "full_name": "Scots gaelic",
        "responses": []
    },
    {
        "country_code": "nso",
        "full_name": "Sepedi",
        "responses": []
    },
    {
        "country_code": "sr",
        "full_name": "Serbian",
        "responses": []
    },
    {
        "country_code": "st",
        "full_name": "Sesotho",
        "responses": []
    },
    {
        "country_code": "sn",
        "full_name": "Shona",
        "responses": []
    },
    {
        "country_code": "sd",
        "full_name": "Sindhi",
        "responses": []
    },
    {
        "country_code": "si",
        "full_name": "Sinhala",
        "responses": []
    },
    {
        "country_code": "sk",
        "full_name": "Slovak",
        "responses": []
    },
    {
        "country_code": "sl",
        "full_name": "Slovenian",
        "responses": []
    },
    {
        "country_code": "so",
        "full_name": "Somali",
        "responses": []
    },
    {
        "country_code": "es",
        "full_name": "Spanish",
        "responses": []
    },
    {
        "country_code": "su",
        "full_name": "Sundanese",
        "responses": []
    },
    {
        "country_code": "sw",
        "full_name": "Swahili",
        "responses": []
    },
    {
        "country_code": "sv",
        "full_name": "Swedish",
        "responses": []
    },
    {
        "country_code": "tg",
        "full_name": "Tajik",
        "responses": []
    },
    {
        "country_code": "ta",
        "full_name": "Tamil",
        "responses": []
    },
    {
        "country_code": "tt",
        "full_name": "Tatar",
        "responses": []
    },
    {
        "country_code": "te",
        "full_name": "Telugu",
        "responses": []
    },
    {
        "country_code": "th",
        "full_name": "Thai",
        "responses": []
    },
    {
        "country_code": "ti",
        "full_name": "Tigrinya",
        "responses": []
    },
    {
        "country_code": "ts",
        "full_name": "Tsonga",
        "responses": []
    },
    {
        "country_code": "tr",
        "full_name": "Turkish",
        "responses": []
    },
    {
        "country_code": "tk",
        "full_name": "Turkmen",
        "responses": []
    },
    {
        "country_code": "ak",
        "full_name": "Twi",
        "responses": []
    },
    {
        "country_code": "uk",
        "full_name": "Ukrainian",
        "responses": []
    },
    {
        "country_code": "ur",
        "full_name": "Urdu",
        "responses": []
    },
    {
        "country_code": "ug",
        "full_name": "Uyghur",
        "responses": []
    },
    {
        "country_code": "uz",
        "full_name": "Uzbek",
        "responses": []
    },
    {
        "country_code": "vi",
        "full_name": "Vietnamese",
        "responses": []
    },
    {
        "country_code": "cy",
        "full_name": "Welsh",
        "responses": []
    },
    {
        "country_code": "xh",
        "full_name": "Xhosa",
        "responses": []
    },
    {
        "country_code": "yi",
        "full_name": "Yiddish",
        "responses": []
    },
    {
        "country_code": "yo",
        "full_name": "Yoruba",
        "responses": []
    },
    {
        "country_code": "zu",
        "full_name": "Zulu",
        "responses": []
    }
]
