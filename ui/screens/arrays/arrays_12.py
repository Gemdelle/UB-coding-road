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
        if output == "Cantidad inicial: 4\nCantidad final: 0\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_13),
        process_input=process_input,
        level_name="arrays",
        level_number=12,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.13-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.13-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.13 Vaciar un array clear()',
        task_text='❧ Al llegar al final de las vías es necesario vaciar el tren. Vaciar el tren e imprimir la cantidad inicial y final.',
        correct_code_text='tren = [ "alejandrita", "rubí", "diamante", "rubí"]\ncantidad_inicial = len(tren)\ntren.clear()\ncantidad_final = len(tren)\nprint(f"Cantidad inicial: {cantidad_inicial}\nCantidad final: {cantidad_final}")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "alejandrita", "rubí", "diamante", "rubí"]\nprint(f"Cantidad inicial: {cantidad_inicial}\nCantidad final: {cantidad_final}")',
    )
    layout.draw()
