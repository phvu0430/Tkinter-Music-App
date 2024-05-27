from pygame.mixer_music import play
from dal.connect_sqlite3 import ConnectSQLite3
from dto.playlist_dto import PlaylistDTO

class PlaylistBLL:
    def __init__(self):
        self.connectDB = ConnectSQLite3()

    def savePlaylist(self, playlist: PlaylistDTO):
        self.connectDB.savePlaylist(playlist)

    def isPlaylistExisted(self, playlist_name):
        return self.connectDB.isPlaylistExisted(playlist_name)

    def fetchPlaylists(self):
        rows = self.connectDB.fetchPlaylists()
        return rows

    def fetchPlaylist(self, playlist_name):
        rows = self.connectDB.fetchPlaylist(playlist_name)
        return rows

    def deletePlaylist(self, playlist_name):
        self.connectDB.deletePlaylist(playlist_name)


