

def cleanString(text: str):
    replacement = "_"
    replacements = [" ", ":", ",", ".", ""]
    for r in replacements:
        while not text.__contains__(r):
            text = text.replace(r, replacement)
    return text
    