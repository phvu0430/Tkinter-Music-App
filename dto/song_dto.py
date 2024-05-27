class SongDTO:
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def getName(self):
        return self.name

    def getPath(self):
        return self.path
