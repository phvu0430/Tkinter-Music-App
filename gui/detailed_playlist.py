from tkinter import *
from PIL import Image, ImageTk
from ttkbootstrap.constants import *
from tkinter import filedialog
from tkinter import messagebox
from dto.playlist_dto import PlaylistDTO
from dto.song_dto import SongDTO
from bll.song_bll import SongBLL
import tkinter.ttk as ttk
from mutagen.mp3 import MP3
import time
import ttkbootstrap as tb
import pygame
import os

class DetailedPlaylist_Frame(tb.Frame):
    def __init__(self, master, playlist):
        super().__init__(master)

        self.playlist = playlist
        self.isPaused = False
        self.is_shuffled = False
        self.is_repeated = False

        pygame.mixer.init()

        self.songbll = SongBLL()

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

        self.feature_name = tb.Label(self.top_container, text=self.playlist, font=("Helvetica", 30, "bold italic"))
        self.feature_name.grid(row=0, column=0, padx=(45, 20), pady=(10, 0))

        self.search_bar_container = tb.Frame(self.top_container)
        self.search_bar_container.grid(row=0, column=1, padx=(50, 0), pady=(10, 0))

        self.search_bar = tb.Entry(self.search_bar_container, width=40)
        self.search_bar.grid(row=0, column=0, padx=10)

        self.search_btn = tb.Button(self.search_bar_container, image=self.icon_images["search-btn"], command=self.search)
        self.search_btn.grid(row=0, column=1, padx=10)

        self.refresh_btn = tb.Button(self.search_bar_container, image=self.icon_images["refresh-btn"], command=self.refresh)
        self.refresh_btn.grid(row=0, column=2, padx=10)

        self.back_btn = tb.Button(self.top_container, text="Back", command=self.back)
        self.back_btn.grid(row=1, column=0, pady=10)

        self.add_song_btn = tb.Button(self.top_container, text="Add song", command=self.add_song)
        self.add_song_btn.grid(row=1, column=1, pady=10)

        self.delete_song = tb.Button(self.top_container, text="Delete song", command=self.delete_song)
        self.delete_song.grid(row=1, column=2, pady=10)

        self.song_box = Listbox(self.top_container, fg="green", height=20, width=100)
        self.song_box.grid(row=2, column=1, padx=(0, 10), pady=10)

        songs = self.songbll.fetchSongsInPlaylist(self.playlist)
        for song in songs:
            self.song_box.insert(END, song[0])

        # Buttons Container
        self.initBtnContainer()


    def back(self):
        self.destroy()

    def add_song(self):
        song_path = filedialog.askopenfilename(initialdir="~/Music", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"), ))
        song_name = song_path.split("/")
        song_name = song_name[-1]
        song_name = song_name.split(".")
        song_name = song_name[0]


        if not self.songbll.isSongExisted(song_name):
            song = SongDTO(song_name, song_path)
            self.songbll.saveSong(song)

        self.songbll.addSongToPlaylist(self.playlist, song_name)
        self.song_box.insert(END, song_name)

    def delete_song(self):
        selected_index = self.song_box.curselection()
        if selected_index:
            self.songbll.deleteSongInPlaylist(self.playlist, self.song_box.get(ACTIVE))
            self.song_box.delete(selected_index)

    def refresh(self):
        self.song_box.delete(0, END)
        songs = self.songbll.fetchSongsInPlaylist(self.playlist)
        for song in songs:
            self.song_box.insert(END, song[0])

    def search(self):
        self.song_box.delete(0, END)
        songs = self.songbll.fetchSongInPlaylist(self.playlist, self.search_bar.get())
        for song in songs:
            self.song_box.insert(END, song[1])

    def initBtnContainer(self):
        self.btn_container_frame = tb.Frame(self.top_container)
        self.btn_container_frame.grid(row=3, column=1, sticky="nsew", pady=(10, 0))
        
        self.current_song = tb.Label(self.btn_container_frame)
        self.current_song.pack(pady=10)

        self.slider = ttk.Scale(self.btn_container_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=self.slide, length=500)
        self.slider.pack(pady=10)

        self.status_bar = tb.Label(self.btn_container_frame, font=("Helvetica", 18))
        self.status_bar.pack(pady=5)

        self.btn_container = tb.Frame(self.btn_container_frame)
        self.btn_container.pack()

        self.shuffle_btn = tb.Label(self.btn_container, image=self.icon_images['shuffle'])
        self.shuffle_btn.grid(row=0, column=0, padx=5)
        self.shuffle_btn.bind("<Enter>", self.on_enter)
        self.shuffle_btn.bind("<Leave>", self.on_leave)
        self.shuffle_btn.bind("<Button-1>", self.on_click_shuffle)

        self.previous_btn = tb.Label(self.btn_container, image=self.icon_images['previous'])
        self.previous_btn.grid(row=0, column=1, padx=5)
        self.previous_btn.bind("<Enter>", self.on_enter)
        self.previous_btn.bind("<Leave>", self.on_leave)
        self.previous_btn.bind("<Button-1>", self.on_click_previous)

        self.play_btn = tb.Label(self.btn_container, image=self.icon_images['play'])
        self.play_btn.grid(row=0, column=2, padx=5)
        self.play_btn.bind("<Enter>", self.on_enter)
        self.play_btn.bind("<Leave>", self.on_leave)
        self.play_btn.bind("<Button-1>", self.on_click_play)
        
        self.pause_btn = tb.Label(self.btn_container, image=self.icon_images['pause'])
        self.pause_btn.grid(row=0, column=3, padx=5)
        self.pause_btn.bind("<Enter>", self.on_enter)
        self.pause_btn.bind("<Leave>", self.on_leave)
        self.pause_btn.bind("<Button-1>", self.on_click_pause)

        self.next_btn = tb.Label(self.btn_container, image=self.icon_images['next'])
        self.next_btn.grid(row=0, column=4, padx=5)
        self.next_btn.bind("<Enter>", self.on_enter)
        self.next_btn.bind("<Leave>", self.on_leave)
        self.next_btn.bind("<Button-1>", self.on_click_next)

        self.repeat_btn = tb.Label(self.btn_container, image=self.icon_images['repeat'])
        self.repeat_btn.grid(row=0, column=5, padx=5)
        self.repeat_btn.bind("<Enter>", self.on_enter)
        self.repeat_btn.bind("<Leave>", self.on_leave)
        self.repeat_btn.bind("<Button-1>", self.on_click_repeat)

    def on_enter(self, event):
        event.widget.config(cursor="hand2")  # Change to pointer cursor

    def on_leave(self, event):
        event.widget.config(cursor="")  # Reset to default cursor

  
    def play_time(self):
        current_time = pygame.mixer.music.get_pos() / 1000

        converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))
        curent_song = self.song_box.curselection()
        song_name = self.song_box.get(curent_song)
        song_path = self.songbll.getSongPath(song_name)
        self.song_length = MP3(song_path[0][0]).info.length
        self.converted_song_length = time.strftime("%M:%S", time.gmtime(self.song_length))


        current_time += 1

        if int(self.slider.get()) == int(self.song_length):
            self.status_bar.configure(text=f"{self.converted_song_length} / {self.converted_song_length}")
        elif self.isPaused:
            pass
        elif int(self.slider.get()) == int(current_time):
            # slider has not been moved
            slider_position = int(self.song_length)
            self.slider.config(to=slider_position, value=int(current_time))
        else:
            # slider has been moved
            slider_position = int(self.song_length)
            self.slider.config(to=slider_position, value=int(self.slider.get()))

            # convert time to format
            converted_current_time = time.strftime("%M:%S", time.gmtime(int(self.slider.get())))

            # output time to status bar 
            self.status_bar.configure(text=f"{converted_current_time} / {self.converted_song_length}")

            # Move this thing along by one second
            next_time = int(self.slider.get()) + 1
            self.slider.config(to=slider_position, value=next_time)



        # self.slider.config(value=int(current_time))


        # update time 
        self.status_bar.after(1000, self.play_time)

    def slide(self, X):
        # self.slider_lb.config(text=f"{int(self.slider.get())}  of  {self.converted_song_length}")
        song = self.song_box.get(ACTIVE)
        song_path = self.songbll.getSongPath(song)

        pygame.mixer.music.load(song_path[0][0])
        pygame.mixer.music.play(loops=0, start=int(self.slider.get()))


    def on_click_play(self, event):
        song = self.song_box.get(ACTIVE)
        
        self.current_song.config(text=song)
        self.status_bar.config(text="")
        self.slider.config(value=0)

        song_path = self.songbll.getSongPath(song)

        pygame.mixer.music.load(song_path[0][0])
        pygame.mixer.music.play(loops=0)

        self.play_time()

    def on_click_pause(self, event):
        if self.isPaused:
            pygame.mixer.music.unpause()
            self.isPaused = False
        else:
            pygame.mixer.music.pause()
            self.isPaused = True

    def on_click_previous(self, event):
        selected_song = self.song_box.curselection()[0]
        self.song_box.selection_clear(0, END)

        if selected_song > 0:
            selected_song = selected_song - 1
        else:
            selected_song = self.song_box.size() - 1

        self.song_box.selection_set(selected_song)

        song = self.song_box.get(selected_song)
        self.current_song.config(text=song)
        self.status_bar.config(text="")
        self.slider.config(value=0)

        song_path = self.songbll.getSongPath(song)

        pygame.mixer.music.load(song_path[0][0])
        pygame.mixer.music.play(loops=0)

        self.play_time()


    def on_click_next(self, event):
        selected_song = self.song_box.curselection()[0]
        self.song_box.selection_clear(0, END)

        if selected_song == self.song_box.size() - 1:
            selected_song = 0
        else:
            selected_song = selected_song + 1

        self.song_box.selection_set(selected_song)

        song = self.song_box.get(selected_song)
        self.current_song.config(text=song)
        self.status_bar.config(text="")
        self.slider.config(value=0)

        song_path = self.songbll.getSongPath(song)

        pygame.mixer.music.load(song_path[0][0])
        pygame.mixer.music.play(loops=0)

        self.play_time()


    def on_click_shuffle(self, event):
        if not self.is_shuffled:
            self.shuffle_btn.configure(image=self.icon_images["shuffle-yes"])
            self.is_shuffled = True
        else:
            self.shuffle_btn.configure(image=self.icon_images["shuffle"])
            self.is_shuffled = False

    def on_click_repeat(self, event):
        if not self.is_repeated:
            self.repeat_btn.configure(image=self.icon_images["repeat-yes"])
            self.is_repeated = True
        else:
            self.repeat_btn.configure(image=self.icon_images["repeat"])
            self.is_repeated = False







