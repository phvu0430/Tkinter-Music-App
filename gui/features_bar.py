from tkinter import *
from PIL import Image, ImageTk
from .playlist_feature import PlaylistFeature_Frame
from .song_feature import SongFeature_Frame
from ttkbootstrap.constants import *
import ttkbootstrap as tb

class FeaturesBar(tb.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)

        # Icons (assuming these are pre-loaded elsewhere)
        self.icon_images = {
            "home": ImageTk.PhotoImage(Image.open('./gui/img/home.png')),
            "playlists": ImageTk.PhotoImage(Image.open('./gui/img/playlist.png')),
            # "heart": ImageTk.PhotoImage(Image.open('./gui/img/heart.png')),
            # "history": ImageTk.PhotoImage(Image.open('./gui/img/history.png')),
            # "settings": ImageTk.PhotoImage(Image.open('./gui/img/gear.png')),
        }
        self.icon_on_images = {
            "home": ImageTk.PhotoImage(Image.open('./gui/img/home_on.png')),
            "playlists": ImageTk.PhotoImage(Image.open('./gui/img/playlist_on.png')),
            # "heart": ImageTk.PhotoImage(Image.open('./gui/img/heart_on.png')),
            # "history": ImageTk.PhotoImage(Image.open('./gui/img/history_on.png')),
            # "settings": ImageTk.PhotoImage(Image.open('./gui/img/gear_on.png')),
        }

        # Create icon labels
        self.icon_labels = {}  # Dictionary to store label references
        for icon_name, image in self.icon_images.items():
            label = tb.Label(self, image=image)
            label.bind("<Enter>", self.on_enter)
            label.bind("<Leave>", self.on_leave)
            label.bind("<Button-1>", lambda event, icon=icon_name: self.on_click(event, icon))
            label.pack(padx=5, pady=10)
            self.icon_labels[icon_name] = label

        self.feature_frames = {}

        self.playlist_feature_frame = PlaylistFeature_Frame(self.master)
        self.playlist_feature_frame.grid_forget()
        self.song_feature_frame = SongFeature_Frame(self.master)
        self.song_feature_frame.grid_forget()

        self.feature_frames["home"] = self.playlist_feature_frame
        self.feature_frames["playlists"] = self.song_feature_frame


    def on_enter(self, event):
        event.widget.config(cursor="hand2")  # Change to pointer cursor

    def on_leave(self, event):
        event.widget.config(cursor="")  # Reset to default cursor

    def on_click(self, event, icon_name):
        # Update all labels using stored references
        for name, label in self.icon_labels.items():
            if name == icon_name:
                label.config(image=self.icon_on_images[name])
                self.feature_frames[name].grid(row=0, column=1, sticky="nsew")
            else:
                label.config(image=self.icon_images[name])
                self.feature_frames[name].grid_forget()
