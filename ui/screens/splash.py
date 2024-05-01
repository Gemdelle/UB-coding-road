from PIL import Image, ImageTk
import tkinter as tk
from tkinter import YES, BOTH

from core.screens import Screens
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager
from utils.sound_manager import SoundManager


def play_music():
    sound_manager = SoundManager()
    sound_manager.set_volume("introduction", 0.05)
    sound_manager.play_sound("introduction")

def draw(frame, change_screen):
    play_music()

    canvas = tk.Canvas(frame, bg="black", width=1280, height=720)
    canvas.pack(fill=BOTH, expand=YES)

    image = Image.open(resource_path("assets\\images\\splash.png"))
    image = image.resize((1280, 720))
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

    # Start Copyright #
    copyright_image = Image.open(resource_path(f"assets\\images\\copyright\\copyright.png"))
    copyright_image = copyright_image.resize((280, 33))
    copyright_image_tk = ImageTk.PhotoImage(copyright_image)
    setattr(canvas, f"copyright_image_tk", copyright_image_tk)
    canvas.create_image(980, 25, anchor=tk.NW, image=copyright_image_tk)
    # End Copyright #

    set_timeout_manager = SetTimeoutManager()
    set_timeout_manager.setTimeout(lambda: change_screen(Screens.LANDING), 3)
