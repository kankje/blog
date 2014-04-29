import re


def canocalize(s):
    return re.sub(r'[^a-zA-Z0-9-]', r'', re.sub(r'(-)\1+', r'\1', s.replace(' ', '-'))).lower()
