import re


def canocalize(s):
    return re.sub(r'[^a-zA-Z0-9-]', '', s.replace('  ', ' ').replace(' ', '-').replace('_', '-')).lower()
