import re
import unicodedata


def normalize_string(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    name = unicodedata.normalize("NFD", text)
    name = "".join(ch for ch in name if unicodedata.category(ch) != "Mn")
    name = re.sub(r"[^a-z0-9]", "", name)
    return name
