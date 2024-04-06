import tkinter as tk

from core.screens import Screens
from ui.screens import splash, landing, book


class ScreenFrame(tk.Frame):
    def __init__(self, master, screen):
        super().__init__(master, width= 1280, height=720, bg="#3d6466")

        screen_draw_functions = {
            Screens.SPLASH: splash.draw,
            Screens.LANDING: landing.draw,
            Screens.BOOK: book.draw,
        }
        draw_function = screen_draw_functions.get(screen)

        if draw_function:
            draw_function(self)