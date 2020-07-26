class ContentUpdaterMixIn:
    def __init__(self, source):
        self.source = source
        self._contents = []

    @property
    def contents(self):
        return self._contents.copy()

    def update_contents(self, phrase, source):
        self._contents.append(
            {'phrase': phrase, 
            'path': source}
        ) 