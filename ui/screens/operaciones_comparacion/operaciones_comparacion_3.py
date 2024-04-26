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
        if output == "Stock de perfume de fragancia floral para espacio cerrado de valor superior a 5500 e inferior a 6500: True\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_COMPARACION_4),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=3,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-02.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.4 Mayor o igual que (>=)',
        task_text='❧ Declarar y completar las variables necesarias para poder realizar la venta según el pedido del cliente:\n“Estoy buscando un perfume de fragancia floral para usar en un salón cerrado para un casamiento la semana que viene,\ncomo es un evento importante estaría dispuesta a gastar más de $5500 pero menos de $6500, incluidos ambos valores” \n*Tener en cuenta que el dato del salón “cerrado” corresponde a la categoría espacio.\n**Es posible que en este caso haya que declarar un presupuesto máximo y uno mínimo ya que se trata de un rango.',
        correct_code_text='fragancia = "floral"\nespacio = "cerrado"\npresupuesto_maximo = 6500\npresupuesto_minimo= 5500\nprecio = 5680\ncumple_requisitos = presupuesto_maximo >= precio >= presupuesto_minimo\nprint(f"Stock de perfume de fragancia {fragancia} para espacio {espacio} de valor superior a {presupuesto_minimo} e inferior a {presupuesto_maximo}: {cumple_requisitos}")\n',
        incorrect_code_text='print(f"En el negocio hay disponibilidad de perfume de fragancia {} para espacio {} de valor superior a {} e inferior a {}: {}")\n'
    )
    layout.draw()
