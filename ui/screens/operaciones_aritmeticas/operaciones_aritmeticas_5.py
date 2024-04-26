import tkinter as tk
import io
import sys

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
    input_text = input_area.get("1.0", "end-1c")
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(input_text)

        output = captured_output.getvalue()
        if output == "Llaves estándar: 4, Copias estándar: 8\nLlaves deluxe: 2, Copias deluxe: 4\nLlaves suite: 3, Copias suite: 6\nTotal de llaves: 9, Total de copias: 18\n":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_print()
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_6),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=5,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-02.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.6 Potenciación con variables (**)',
        task_text='❧ Un hotel tiene tres tipos de habitaciones: estándar, deluxe y suite. Cada tipo de habitación\ntiene una cierta cantidad de llaves disponibles. Las habitaciones estándar son representadas por llaves comunes,\nlas deluxe son con llaves celestes y las suite son con llaves rojas. Por cada llave disponible de cada\ntipo de habitación, el hotel realiza una copia adicional de esa habitación.\nDeclarar las variables <llaves_estandar>, <llaves_deluxe> y <llaves_suite> con la cantidad de llaves disponibles\npara cada tipo de habitación según la imagen. Declarar también <copias_estandar>, <copias_deluxe> y <copias_suite> para almacenar\nla cantidad de copias adicionales de habitaciones que se generarán.',
        correct_code_text='llaves_estandar = 4\nllaves_deluxe = 2\nllaves_suite = 3\ncopias_estandar = llaves_estandar * 2\ncopias_deluxe = llaves_deluxe * 2\ncopias_suite = llaves_suite * 2\ntotal_llaves = llaves_estandar + llaves_deluxe + llaves_suite\ntotal_copias = copias_estandar + copias_deluxe + copias_suite\nprint(f"Llaves estándar: {llaves_estandar}, Copias estándar: {copias_estandar}")\nprint(f"Llaves deluxe: {llaves_deluxe}, Copias deluxe: {copias_deluxe}")\nprint(f"Llaves suite: {llaves_suite}, Copias suite: {copias_suite}")\nprint(f"Total de llaves: {total_llaves}, Total de copias: {total_copias}")\n',
        incorrect_code_text=''
    )
    layout.draw()
