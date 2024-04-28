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
        if output == "En el negocio hay disponibilidad de perfume de fragancia cítrica para temporada verano para usar en ocasión de día: True\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_COMPARACION_5),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=4,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-6\\06-05-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-6\\06-05-w.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.5 Igual que (==)',
        task_text='❧ Declarar y completar las variables necesarias para poder realizar la venta según el pedido del cliente.\nEn este caso, la caja registradora NO tiene cambio, es decir,\nno se puede devolver vuelto y solo se puede abonar con billetes de $100 o $1000:\n“Estoy buscando un perfume de fragancia cítrica para usar en el verano durante el día, tengo para gastar en efectivo 6880.”',
        correct_code_text='fragancia = "cítrica"\ntemporada = "verano"\nocasion = "día"\nprecio = 6880\npresupuesto = 6880\ncumple_requisitos = precio == presupuesto\nprint(f"En el negocio hay disponibilidad de perfume de fragancia {fragancia} para temporada {temporada} para usar en ocasión de {ocasion}: {cumple_requisitos}")\n',
        incorrect_code_text='print(f"En el negocio hay disponibilidad de perfume de fragancia {} para temporada {} para usar en ocasión de {}: {}")\n'
    )
    layout.draw()
