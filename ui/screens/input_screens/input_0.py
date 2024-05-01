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
        r'input\(',
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
        next_screen=lambda: change_screen(Screens.INPUT_1),
        process_input=process_input,
        level_name="input",
        level_number=0,
        module_number=4,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-n-4\\4-2.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-n-4\\4-1.png"),
        title_text="4. Input",
        subtitle_text='4.1 Ingresar un texto y printearlo',
        task_text='❧ En el lugar donde se está no hay internet.\nHay que mandar una carta, pero para eso hay que escribir\ntodos los datos del destino. Leer por teclado la dirección\na la que se va a enviar e imprimirla así queda\nen el sobre: “Paroissien 2012”.',
        correct_code_text='direccion = input("Ingrese la dirección a donde se enviará la carta: ")\nprint(direccion)',
        change_screen=change_screen,
        incorrect_code_text=''
    )
    layout.draw()
