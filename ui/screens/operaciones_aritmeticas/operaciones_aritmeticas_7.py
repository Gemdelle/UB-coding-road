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
        if output == "Llaves por habitación: 5\nLlaves sobrantes: 0\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_8),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=7,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-07-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-07-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.8 Módulo (%)',
        task_text='❧ Se necesita distribuir uniformemente una cierta cantidad de llaves entre un número determinado de habitaciones en un hotel.\nCada habitación solo puede tener una llave y no pueden quedar llaves sobrantes.\nDeclarar la variable <cantidad_llaves> con el número total de llaves disponibles (10) y la variable <cantidad_habitaciones>\ncon el número total de habitaciones en el hotel (2). Luego, calcular cuántas llaves se asignan asignadas a cada habitación\ny cuántas llaves sobran, si las hay. Asegurate de usar el operador módulo (%) para calcular\nlas llaves sobrantes (calcular <llaves_por_habitacion> y <llaves_sobrantes>).\nImprimir la información con el siguiente formato:\nLlaves por habitación: {x}\nLlaves sobrantes: {y}\n',
        correct_code_text='cantidad_llaves = 10\ncantidad_habitaciones = 2\nllaves_por_habitacion = cantidad_llaves // cantidad_habitaciones\nllaves_sobrantes = cantidad_llaves % cantidad_habitaciones\nprint(f"Llaves por habitación: {llaves_por_habitacion}")\nprint(f"Llaves sobrantes: {llaves_sobrantes}")\n',
        incorrect_code_text=''
    )
    layout.draw()
