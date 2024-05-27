import sqlite3

from pygame.mixer_music import play
from dto.song_dto import SongDTO
from dto.playlist_dto import PlaylistDTO

class ConnectSQLite3:
    def __init__(self):
        self.conn = sqlite3.connect("musicapp.db")

        self.cursor = self.conn.cursor()

        self.createTables()

    def createTables(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS playlists (
                name text PRIMARY KEY)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS songs (
                name text PRIMARY KEY,
                path text)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS detailed_playlists (
                playlist_name text,
                song_name text,
                foreign key (playlist_name) references playlists (name),
                foreign key (song_name) references songs (name)
        )""")

        self.conn.commit()

    def saveSong(self, song: SongDTO):
        self.cursor.execute("INSERT INTO songs (name, path) VALUES (?, ?)", (song.getName(), song.getPath()))
        self.conn.commit()

    def fetchSongs(self):
        self.cursor.execute("SELECT * FROM songs")
        rows = self.cursor.fetchall()
        return rows

    def fetchSong(self, song_name):
        self.cursor.execute("SELECT * FROM songs WHERE name LIKE ?", ('%' + song_name + '%',))
        rows = self.cursor.fetchall()
        return rows

    def fetchPlaylists(self):
        self.cursor.execute("SELECT * FROM playlists")
        rows = self.cursor.fetchall()
        return rows

    def fetchPlaylist(self, playlist_name):
        self.cursor.execute("SELECT * FROM playlists WHERE name LIKE ?", ('%' + playlist_name + '%',))
        rows = self.cursor.fetchall()
        return rows

    def fetchSongsInPlaylist(self, playlist_name):
        self.cursor.execute("SELECT song_name FROM detailed_playlists WHERE playlist_name=?", (playlist_name,))
        rows = self.cursor.fetchall()
        return rows

    def fetchSongInPlaylist(self, playlist_name, song_name):
        self.cursor.execute("SELECT * FROM detailed_playlists WHERE playlist_name = ? and song_name LIKE ?", 
                            (playlist_name, '%' + song_name + '%',))
        rows = self.cursor.fetchall()
        return rows


    def isSongExisted(self, song_name):
        self.cursor.execute("SELECT * FROM songs WHERE name=?", (song_name,))
        rows = self.cursor.fetchall()
        return bool(rows)

    def getSongPath(self, song_name):
        self.cursor.execute("SELECT path FROM songs WHERE name=?", (song_name,))
        rows = self.cursor.fetchall()
        return rows

    def deleteSong(self, song_name):
        self.cursor.execute("delete from songs where name=?", (song_name,))
        self.conn.commit()

    def savePlaylist(self, playlist: PlaylistDTO):
        self.cursor.execute("INSERT INTO playlists (name) VALUES (?)", (playlist.getName(),))
        self.conn.commit()

    def isPlaylistExisted(self, playlist_name):
        self.cursor.execute("select * from playlists where name=?", (playlist_name,))
        rows = self.cursor.fetchall()
        return bool(rows)

    def deletePlaylist(self, playlist_name):
        self.cursor.execute("delete from playlists where name=?", (playlist_name,))
        self.conn.commit()

    def addSongToPlaylist(self, playlist_name, song_name):
        self.cursor.execute("INSERT INTO detailed_playlists (playlist_name, song_name) VALUES (?, ?)", 
                            (playlist_name, song_name,))
        self.conn.commit()

    def deleteSongInPlaylist(self, playlist_name, song_name):
        self.cursor.execute("delete from detailed_playlists where playlist_name=? and song_name=?", 
                            (playlist_name, song_name,))
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()


