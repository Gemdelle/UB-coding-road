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
        if output == "Para 144 habitaciones disponibles, se necesitarían 12.00 llaves en total.\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_7),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=6,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-06-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-06-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.7 Raíz (potenciación) con variables (**)',
        task_text='❧  Ahora se necesita determinar cuántas llaves serían necesarias en función de la cantidad de habitaciones disponibles.\nCada habitación en el hotel requiere una llave para su acceso. Declarar la variable <habitaciones_disponibles> con el número total de habitaciones en el hotel (144).\nLuego, calcular la cantidad máxima de llaves, <llaves necesarias> utilizando la raíz cuadrada como potenciación.\nTip: Elevar el número de habitaciones disponibles a la potencia de 0.5, devuelve la cantidad de llaves necesarias para cubrir todas las habitaciones.\nImprimir la información con el siguiente formato: Para {x} habitaciones disponibles, se necesitarían {y} llaves en total.',
        correct_code_text='habitaciones_disponibles = 144\nllaves_necesarias = habitaciones_disponibles ** 0.5 #esto da 12\nprint(f"Para {habitaciones_disponibles} habitaciones disponibles, se necesitarían {llaves_necesarias:.2f} llaves en total.")\n',
        incorrect_code_text=''
    )
    layout.draw()
