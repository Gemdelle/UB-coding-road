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
        if output == "Tren: ['puro', 'puro', 'puro']\nEl tren está lleno: False\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_20),
        process_input=process_input,
        level_name="arrays",
        level_number=19,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.20-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.20-w.png"),
        title_text="9. Elemento - Modificación",
        subtitle_text='9.20 Eliminar el elemento con el valor especificado (primera aparición) remove()',
        task_text='❧ Se recibieron quejas del laboratorio al que se exportan los minerales diciendo que los minerales impuros (con colores) no sirven para ser analizados. El tren actual tiene minerales impuros, pero se encontró un mineral puro que se puede agregar en el lugar de un impuro. Además, el laboratorio paga extra cuando un tren está lleno; un tren se considera lleno cuando lleva 4 elementos. Eliminar los minerales impuros del <tren> y agregar el mineral puro. Se pide imprimir el <tren> y su estado.',
        correct_code_text='tren = [ "puro", "impuro", "impuro", "puro"]\ntren.remove("impuro")\ntren.remove("impuro")\ntren.append("puro")\nesta_lleno = len(tren) == 4\nprint(f"Tren: {tren}\nEl tren está lleno: {esta_lleno}")',
        change_screen=change_screen,
        incorrect_code_text='ren = [ "puro", "impuro", "impuro", "puro"]\nprint(f"Tren: {tren}\nEl tren está lleno: {esta_lleno}")',
    )
    layout.draw()
