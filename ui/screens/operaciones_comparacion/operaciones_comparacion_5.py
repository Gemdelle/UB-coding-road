import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound


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
    except Exception as e:
        incorrect()
        play_wrong_sound()

def draw(frame, change_screen):
    layout = ScreenLayout(
        frame=frame,
        back_screen=lambda: change_screen(Screens.LANDING),
        next_screen=lambda: change_screen(Screens.WIN_EMBLEM),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=5,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-6\\06-06-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-6\\06-06-w.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.6 No igual que (!=)',
        task_text='❧ Declarar y completar las variables necesarias para poder realizar la venta según el pedido del cliente.\nEssence está lanzando una nueva campaña “OraNge” y por el día de hoy solo se venderá el perfume cítrico de naranja.\nRequerimientos del cliente:\n“Estoy buscando un perfume de nicho que no sea cítrico porque me produce alergia.“',
        correct_code_text='fragancia = "cítrica"\nfragancia_descartada = "cítrica"\ncumple_requisitos = fragancia != fragancia_descartada\nprint(f"En el negocio hay disponibilidad de perfume de fragancia diferente del tipo {fragancia_descartada}: {cumple_requisitos}")\n',
        incorrect_code_text='fragancia_descartada = "cítrica"\nprint(f“En el negocio hay disponibilidad de perfume de fragancia diferente del tipo {}: {}”)\n',
        extra_task_text='*Recordar que los\noperadores de comparación\nno se usan únicamente\ncon números, también\nse pueden utilizar con\ndatos de tipo string.'
    )
    layout.draw()
