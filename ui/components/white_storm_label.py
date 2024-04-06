import os
import tkinter as tk
from tkinter import font

from utils.resource_path_util import resource_path


class WhiteStormLabel(tk.Label):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        #font_path = resource_path("assets\\font\\White Storm.ttf")

        self.custom_font = font.Font(family="Arial", size=20)