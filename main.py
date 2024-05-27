from tkinter import *
from ttkbootstrap.constants import *
from gui.features_bar import FeaturesBar
import ttkbootstrap as tb



root = tb.Window(themename='darkly')


root.title('Music App')
root.geometry('500x500')

# features bar
featuresBar = FeaturesBar(root)
featuresBar.grid(row=0, column=0, sticky="nsew", padx=5)




root.mainloop()
