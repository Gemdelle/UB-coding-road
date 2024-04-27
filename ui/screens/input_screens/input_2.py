import tkinter as tk
import io
import sys
import re

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound

def process_input(input_area, process_button, code_canvas, correct, incorrect):
    patterns = [
        r'direccion\s*=\s*',
        r'print\(',
        r'precio\s*=\s*',
        r'print\(',
        r'precio_express\s*=\s*float\(input\(',
        r'print\('
    ]

    input_text = input_area.get("1.0", "end-1c")

    all_patterns_present = all(re.search(pattern, input_text) is not None for pattern in patterns)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        if all_patterns_present:
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_input()
            play_correct_sound()
        else:
            incorrect()
            play_wrong_sound()
    except Exception as e:
        incorrect()
        play_wrong_sound()

def draw(frame, change_screen):
    layout = ScreenLayout(
        frame=frame,
        back_screen=lambda: change_screen(Screens.LANDING),
        next_screen=lambda: change_screen(Screens.WIN_EMBLEM),
        process_input=process_input,
        level_name="input",
        level_number=2,
        module_number=4,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-n-4\\4-4.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-n-4\\4-3.png"),
        title_text="4. Input",
        subtitle_text='4.3 Ingresar un número en str y transformarlo después a float',
        task_text='❧ Otro dato necesario es el precio extra por envío express,\n <precio_express>, ya que tiene que llegar cuanto antes. Leer por teclado\nel precio del envío express, que corresponde a 600.5 pesos.',
        correct_code_text='direccion = "Paroissien 2012"\nprint(direccion)\nprecio = 2000\nprint(precio)\nprecio_express = float(input("Ingrese el precio de envío: "))\nprint(precio_express)',
        incorrect_code_text='direccion = "Paroissien 2012"\nprint(direccion)\nprecio = 2000\nprint(precio)'
    )
    layout.draw()
