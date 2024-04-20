import tkinter as tk
import io
import sys
import re

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager
from utils.sound_manager import play_correct_sound, play_wrong_sound

def showWrongMessage(code_frame):
    # TODO: Replace message with png word
    error_message_canvas = tk.Canvas(code_frame, width=100, height=30)
    error_message_canvas.create_text(0, 15, text="Try again", fill="#7A0D13", font=("Georgia", 16, "bold"), anchor="w")
    wrong_message_id = code_frame.create_window(500, 620, window=error_message_canvas, anchor="w")
    set_timeout_manager = SetTimeoutManager()
    set_timeout_manager.setTimeout(lambda: code_frame.delete(wrong_message_id), 2)
def process_input(input_area, process_button, code_canvas, correct, incorrect):
    patterns = [
        r'direccion\s*=\s*',
        r'input\(',
        r'print\(',
        r'precio\s*=\s*int\(input\(',
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
            showWrongMessage(code_canvas)
    except Exception as e:
        incorrect()
        play_wrong_sound()
        showWrongMessage(code_canvas)

def draw(frame, change_screen):
    layout = ScreenLayout(
        frame=frame,
        back_screen=lambda: change_screen(Screens.LANDING),
        next_screen=lambda: change_screen(Screens.INPUT_2),
        process_input=process_input,
        level_name="input",
        level_number=1,
        module_number=4,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-n-4\\4-3.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-n-4\\4-2.png"),
        title_text="4. Input",
        subtitle_text='4.2 Ingresar un número en str y transformarlo después a int',
        task_text='❧ En el sobre hay que anotar el precio de envío.\nLeer por teclado el precio de envío, <precio>,\nque corresponde a 2000 pesos.',
        correct_code_text='direccion = "Paroissien 2012"\nprint(direccion)\nprecio = int(input("Ingrese el precio de envío: "))\nprint(precio)',
        incorrect_code_text='direccion = "Paroissien 2012"\nprint(direccion)'
    )
    layout.draw()