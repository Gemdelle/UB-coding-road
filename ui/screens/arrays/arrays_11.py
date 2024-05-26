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
        if output == "Registro: ['diamante', 'espinela', 'zafiro', 'amatista']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_12),
        process_input=process_input,
        level_name="arrays",
        level_number=11,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.12-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.12-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.12 Revertir el orden un array reverse()',
        task_text='❧ El encargado de cargar las gemas se confundió y las cargó al revés. Además, en el último lugar puso una espinela en lugar de un diamante. Reemplazar la última espinela por diamante (mediante la notación de arrays), invertir el orden para que se impriman correctamente.',
        correct_code_text='tren = [ "amatista", "zafiro", "espinela", "espinela"]\ntren[3] = "diamante"\ntren.reverse()\nprint(f"Registro: {tren}")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "amatista", "zafiro", "espinela", "espinela"]\nprint(f"Registro: {tren}")',
    )
    layout.draw()
