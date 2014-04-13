import re


class Canocalizer:
    def canocalize(self, string):
        return re.sub(r'[^a-zA-Z0-9-]', '', string.replace(' ', '-')).lower()
