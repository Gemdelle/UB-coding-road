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
        if output == "En el negocio hay disponibilidad de perfume de temporada verano de valor inferior o igual a 7450: True\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_COMPARACION_2),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=1,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-6\\06-02-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-6\\06-02-w.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.2 Menor o igual que (<=)',
        task_text='❧ Declarar y completar las variables necesarias para poder realizar la venta según el pedido del cliente:\n“Estoy buscando un perfume para usar este verano, tengo $7450.',
        correct_code_text='temporada = "verano"\npresupuesto = 7450\nprecio = 7450\ncumple_requisitos = precio <= presupuesto\nprint(f"En el negocio hay disponibilidad de perfume de temporada {temporada} de valor inferior o igual a {presupuesto}: {cumple_requisitos}")\n',
        change_screen=change_screen,
        incorrect_code_text='temporada = ""\n#print(f"Stock de perfume {} de valor inferior a {}: {}")\n'
    )
    layout.draw()
