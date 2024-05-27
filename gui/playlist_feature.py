from tkinter import *
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox
from .detailed_playlist import DetailedPlaylist_Frame
from dto.playlist_dto import PlaylistDTO
from bll.playlist_bll import PlaylistBLL
import ttkbootstrap as tb
import pygame
import os

class PlaylistFeature_Frame(tb.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        pygame.mixer.init()

        self.playlistbll = PlaylistBLL()

        self.__initComponents()

    def __initComponents(self):
        self.top_container = tb.Frame(self)
        self.top_container.pack()

        self.icon_images = {
            "search-btn": ImageTk.PhotoImage(Image.open('./gui/img/loupe.png')),
            "refresh-btn": ImageTk.PhotoImage(Image.open('./gui/img/refresh-button.png')),
            "shuffle": ImageTk.PhotoImage(Image.open('./gui/img/shuffle-no.png')),
            "shuffle-yes": ImageTk.PhotoImage(Image.open('./gui/img/shuffle.png')),
            "previous": ImageTk.PhotoImage(Image.open('./gui/img/previous.png')),
            "play": ImageTk.PhotoImage(Image.open('./gui/img/play-button-arrowhead.png')),
            "next": ImageTk.PhotoImage(Image.open('./gui/img/next.png')),
            "repeat": ImageTk.PhotoImage(Image.open('./gui/img/repeat.png')),
            "repeat-yes": ImageTk.PhotoImage(Image.open('./gui/img/repeat-once.png')),
            "speaker": ImageTk.PhotoImage(Image.open('./gui/img/sound.png')),
            "pause": ImageTk.PhotoImage(Image.open('./gui/img/pause.png')),
        }

        self.feature_name = tb.Label(self.top_container, text="Playlists", font=("Helvetica", 30, "bold italic"))
        self.feature_name.grid(row=0, column=0, padx=(45, 20), pady=(10, 0))

        self.search_bar_container = tb.Frame(self.top_container)
        self.search_bar_container.grid(row=0, column=1, padx=(50, 0), pady=(10, 0))

        self.search_bar = tb.Entry(self.search_bar_container, width=40)
        self.search_bar.grid(row=0, column=0, padx=10)

        self.search_btn = tb.Button(self.search_bar_container, image=self.icon_images["search-btn"], command=self.search)
        self.search_btn.grid(row=0, column=1, padx=10)

        self.refresh_btn = tb.Button(self.search_bar_container, image=self.icon_images["refresh-btn"], command=self.refresh)
        self.refresh_btn.grid(row=0, column=2, padx=10)

        self.add_playlist_btn = tb.Button(self.top_container, text="Add playlist", command=self.add_playlist)
        self.add_playlist_btn.grid(row=1, column=0, pady=10)

        self.delete_playlist = tb.Button(self.top_container, text="Delete playlist", command=self.delete_playlist)
        self.delete_playlist.grid(row=1, column=1, pady=10)

        self.playlist_box = Listbox(self.top_container, fg="green", height=20, width=100)
        self.playlist_box.grid(row=2, column=1, padx=(0, 10), pady=10)
        self.playlist_box.bind("<Double-Button-1>", self.on_double_click)

        playlists = self.playlistbll.fetchPlaylists()
        for playlist in playlists:
            self.playlist_box.insert(END, playlist[0])



    def add_playlist(self):
        playlist_name = simpledialog.askstring("Input", "Enter playlist name:")
        if self.playlistbll.isPlaylistExisted(playlist_name):
            messagebox.showerror("Error", "Playlist is already existed !")
        else:
            playlist = PlaylistDTO(playlist_name)
            self.playlistbll.savePlaylist(playlist)

            self.playlist_box.insert(END, playlist.getName())

    def delete_playlist(self):
        selected_index = self.playlist_box.curselection()
        if selected_index:
            self.playlistbll.deletePlaylist(self.playlist_box.get(ACTIVE))
            self.playlist_box.delete(selected_index)



    def refresh(self):
        self.playlist_box.delete(0, END)
        playlists = self.playlistbll.fetchPlaylists()
        for playlist in playlists:
            self.playlist_box.insert(END, playlist[0])

    def search(self):
        self.playlist_box.delete(0, END)
        playlists = self.playlistbll.fetchPlaylist(self.search_bar.get())
        for playlist in playlists:
            self.playlist_box.insert(END, playlist[0])



    def on_double_click(self, event):
        widget = event.widget
        selection = widget.curselection()

        if selection:
            index = selection[0]
            value = widget.get(index)
            self.detailed_playlist_frame = DetailedPlaylist_Frame(self.master, value)
            self.detailed_playlist_frame.grid(row=0, column=1, sticky="nsew")
