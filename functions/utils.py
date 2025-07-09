import re
from unidecode import unidecode

def slugify(text):
    text = unidecode(text).lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_-]+","-", text).strip("-")