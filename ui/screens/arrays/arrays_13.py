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
        if output == "[0.5, 0.5, 1.0, 0.5]\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_14),
        process_input=process_input,
        level_name="arrays",
        level_number=13,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.14-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.14-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.14 Transformación de todos los valores de un array con operadores map()',
        task_text='❧ Para que los análisis sean más precisos, desde el laboratorio se pide duplicar la muestra de cada elemento. Duplicar la cantidad de elementos que hay en cada espacio e imprimir el <tren>.',
        correct_code_text='tren = [1,1,2,1]\ntren = list(map(lambda elemento: elemento / 2, tren))\nprint(tren)',
        change_screen=change_screen,
        incorrect_code_text='tren = [1,1,2,1]\nprint(tren)',
    )
    layout.draw()
