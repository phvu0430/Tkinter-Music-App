from dal.connect_sqlite3 import ConnectSQLite3
from dto.song_dto import SongDTO

class SongBLL:
    def __init__(self):
        self.connectDB = ConnectSQLite3()

    def saveSong(self, song: SongDTO):
        self.connectDB.saveSong(song)

    def fetchSongs(self):
        songs = self.connectDB.fetchSongs()
        return songs

    def fetchSong(self, song_name):
        songs = self.connectDB.fetchSong(song_name)
        return songs

    def fetchSongsInPlaylist(self, playlist_name):
        songs = self.connectDB.fetchSongsInPlaylist(playlist_name)
        return songs

    def isSongExisted(self, song_name):
        return self.connectDB.isSongExisted(song_name)

    def getSongPath(self, song_name):
        return self.connectDB.getSongPath(song_name)

    def deleteSong(self, song_name):
        self.connectDB.deleteSong(song_name)

    def addSongToPlaylist(self, playlist_name, song_name):
        self.connectDB.addSongToPlaylist(playlist_name, song_name)

    def deleteSongInPlaylist(self, playlist_name, song_name):
        self.connectDB.deleteSongInPlaylist(playlist_name, song_name)

    def fetchSongInPlaylist(self, playlist_name, song_name):
        return self.connectDB.fetchSongInPlaylist(playlist_name, song_name)
