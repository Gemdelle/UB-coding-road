from tkinter import BOTH, YES

import tkinter as tk
from PIL import Image, ImageTk

from core.screens import Screens
from utils.resource_path_util import resource_path
from utils.sound_manager import play_button_sound


def draw(frame, change_screen):
    canvas = tk.Canvas(frame, bg="black", width=1280, height=720)
    canvas.pack(fill=BOTH, expand=YES)

    # Start Background #
    image = Image.open(resource_path(f"assets\\images\\backgrounds\\background-notes.png"))
    image = image.resize((1280, 720))
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)
    # End Background #

    # Start Back Arrow #
    back_arrow_image = Image.open(resource_path("assets\\images\\back_arrow.png"))
    back_arrow_image = back_arrow_image.resize((59, 33))
    back_arrow_image_tk = ImageTk.PhotoImage(back_arrow_image)

    def on_back_arrow_click(event):
        play_button_sound()
        change_screen(Screens.LANDING)
        canvas.destroy()

    def on_arrow_click_image_enter(event):
        canvas.config(cursor="hand2")

    def on_arrow_click_image_leave(event):
        canvas.config(cursor="")

    setattr(canvas, f"back_arrow_image_library_tk", back_arrow_image_tk)
    back_arrow_button = canvas.create_image(45, 57, anchor="w", image=back_arrow_image_tk)
    canvas.tag_bind(back_arrow_button, "<Enter>", on_arrow_click_image_enter)
    canvas.tag_bind(back_arrow_button, "<Leave>", on_arrow_click_image_leave)
    canvas.tag_bind(back_arrow_button, '<Button-1>', on_back_arrow_click)
    # End Back Arrow #

    # Start Code Area #
    text_area = tk.Text(canvas, wrap="word", width=30, height=23, borderwidth=0, highlightthickness=0, font=("Georgia", 10), bg="#b2b18e")
    canvas.create_window(412, 355, window=text_area, anchor=tk.CENTER)
    # End Code Area #

    # Start Code Area # #b2b18e
    text_area = tk.Text(canvas, wrap="word", width=30, height=23, borderwidth=0, highlightthickness=0,
                        font=("Georgia", 10), bg="#b2b18e")
    canvas.create_window(858, 355, window=text_area, anchor=tk.CENTER)
    # End Code Area #