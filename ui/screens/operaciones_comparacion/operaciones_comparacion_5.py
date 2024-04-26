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
        if output == "En el negocio hay disponibilidad de perfume de fragancia diferente del tipo cítrica: False\n":
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
        next_screen=lambda: change_screen(Screens.LANDING),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=5,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-02.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.6 No igual que (!=)',
        task_text='❧ Declarar y completar las variables necesarias para poder realizar la venta según el pedido del cliente.\nEssence está lanzando una nueva campaña “OraNge” y por el día de hoy solo se venderá el perfume cítrico de naranja.\nRequerimientos del cliente:\n“Estoy buscando un perfume de nicho que no sea cítrico porque me produce alergia.“\n*Recordar que los operadores de comparación no se usan únicamente con números, también se pueden utilizar con datos de tipo string.',
        correct_code_text='fragancia = "cítrica"\nfragancia_descartada = "cítrica"\ncumple_requisitos = fragancia != fragancia_descartada\nprint(f"En el negocio hay disponibilidad de perfume de fragancia diferente del tipo {fragancia_descartada}: {cumple_requisitos}")\n',
        incorrect_code_text='fragancia_descartada = "cítrica"\nprint(f“En el negocio hay disponibilidad de perfume de fragancia diferente del tipo {}: {}”)\n'
    )
    layout.draw()
