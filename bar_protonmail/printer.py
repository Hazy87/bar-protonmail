import json


class Printer:
    def _print(self, text):
        try:
            print(text, flush=True)
        except BrokenPipeError:
            pass


class WaybarPrinter(Printer):
    def __init__(self, badge: str, hide_if_empty: bool):
        self.badge = badge
        self.hide_if_empty = hide_if_empty

    def print(self, count, inaccurate=False):
        classes = set()
        text = ''
        if inaccurate:
            classes.add('inaccurate')
        if count > 0:
            classes.add('unread')
            text = str(count)
        if count == 0 and self.hide_if_empty:
            self._print(text)
            return
        text = f'{self.badge} {text}'.strip()
        text = json.dumps({'text': f'{text}', 'class': list(classes)})
        self._print(text)

    def error(self, message):
        text = json.dumps({'text': message, 'class': 'error'})
        self._print(text)


class PolybarPrinter(Printer):
    def __init__(self, badge: str, hide_if_empty: bool, color: str = None, ):
        self.badge = badge
        self.color = color
        self.hide_if_empty = hide_if_empty

    def print(self, count, inaccurate=False):
        text = str(count) if count > 0 else ''
        if inaccurate:
            text = f'~{text}'
        text = f'{self.badge} {text}'.strip()
        if count > 0 and self.color:
            text = f'%{{F{self.color}}}{text}%{{F-}}'
        self._print(text)

    def error(self, message):
        text = f' {message}'
        if self.color:
            text = f'%{{F{self.color}}}{text}%{{F-}}'
        self._print(text)
