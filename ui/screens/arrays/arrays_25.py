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
        if output == "Juntar 4 minerales impuros y mandarlos  a la central\n":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_arrays()
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
        next_screen=lambda: change_screen(Screens.ARRAYS_26),
        process_input=process_input,
        level_name="arrays",
        level_number=25,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.26-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.26-w.png"),
        title_text="9. Transformación - String y Array",
        subtitle_text='9.26 Unir elementos de un array en un único string join()',
        task_text='❧ El laboratorio ahora envía notas enteras en lugar de listas, pero siempre se desarman por la humedad. Imprimir el mensaje reconstruido uniendo los papelitos y juntar lo que se pide.',
        correct_code_text='pedacitos_de_papel = ["Juntar 4 minerales impuros", "y mandarlos ", "a la central"]\ntren = ["mineral impuro,"mineral impuro,"mineral impuro,"mineral impuro"]\nmensaje_unido = " ".join(pedacitos_de_papel)\nprint(mensaje_unido)',
        change_screen=change_screen,
        incorrect_code_text='pedacitos_de_papel = ["Juntar 4 minerales impuros", "y mandarlos ", "a la central"]\ntren = []\nprint(mensaje_unido)',
    )
    layout.draw()
