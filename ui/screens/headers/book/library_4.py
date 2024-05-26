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
    image = Image.open(resource_path(f"assets\\images\\book\\book-9.7-9.8.png"))
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

    setattr(canvas, f"back_arrow_image_programme_tk", back_arrow_image_tk)
    back_arrow_button = canvas.create_image(45, 57, anchor="w", image=back_arrow_image_tk)
    canvas.tag_bind(back_arrow_button, "<Enter>", on_arrow_click_image_enter)
    canvas.tag_bind(back_arrow_button, "<Leave>", on_arrow_click_image_leave)
    canvas.tag_bind(back_arrow_button, '<Button-1>', on_back_arrow_click)
    # End Back Arrow #

    create_next_arrow(canvas, change_screen)
    create_back_arrow(canvas, change_screen)

def create_back_arrow(canvas, change_screen):
    image_next_arrow = Image.open(resource_path("assets\\images\\back_arrow.png"))
    image_next_arrow = image_next_arrow.resize((75, 42))
    image_next_arrow_tk = ImageTk.PhotoImage(image_next_arrow)

    def on_image_next_arrow_click(event):
        play_button_sound()
        change_screen(Screens.LIBRARY_3)
        canvas.destroy()

    def on_image_next_arrow_enter(event):
        canvas.config(cursor="hand2")

    def on_image_next_arrow_leave(event):
        canvas.config(cursor="")

    setattr(canvas, f"image_next_arrow_tk", image_next_arrow_tk)
    next_arrow_button = canvas.create_image(40, 350, anchor=tk.NW, image=image_next_arrow_tk)
    canvas.tag_bind(next_arrow_button, '<Button-1>', on_image_next_arrow_click)
    canvas.tag_bind(next_arrow_button, "<Enter>", on_image_next_arrow_enter)
    canvas.tag_bind(next_arrow_button, "<Leave>", on_image_next_arrow_leave)


def create_next_arrow(canvas, change_screen):
    image_next_arrow = Image.open(resource_path("assets\\images\\next_arrow.png"))
    image_next_arrow = image_next_arrow.resize((75, 42))
    image_next_arrow_tk = ImageTk.PhotoImage(image_next_arrow)

    def on_image_next_arrow_click(event):
        play_button_sound()
        change_screen(Screens.LIBRARY_5)
        canvas.destroy()

    def on_image_next_arrow_enter(event):
        canvas.config(cursor="hand2")

    def on_image_next_arrow_leave(event):
        canvas.config(cursor="")

    setattr(canvas, f"image_next_arrow_programme_tk", image_next_arrow_tk)
    next_arrow_button = canvas.create_image(1180, 350, anchor=tk.NW, image=image_next_arrow_tk)
    canvas.tag_bind(next_arrow_button, '<Button-1>', on_image_next_arrow_click)
    canvas.tag_bind(next_arrow_button, "<Enter>", on_image_next_arrow_enter)
    canvas.tag_bind(next_arrow_button, "<Leave>", on_image_next_arrow_leave)