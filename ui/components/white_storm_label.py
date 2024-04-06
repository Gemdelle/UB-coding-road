import tkinter as tk
from tkinter import font


class WhiteStormLabel(tk.Label):
    def __init__(self, master=None, bg=None, font_size=None, **kwargs):
        super().__init__(master, bg=bg, **kwargs)

        self.custom_font = font.Font(family="White Storm", size=font_size)
        self.custom_font = font.Font(family="Georgia", size=font_size)
        self.config(font=self.custom_font)  # Aplicar la fuente al widget
