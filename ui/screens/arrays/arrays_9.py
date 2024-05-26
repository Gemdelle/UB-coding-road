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
        if output == "El tren lleva 4 gemas: diamante, zafiro, rubí, alejandrita\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_10),
        process_input=process_input,
        level_name="arrays",
        level_number=9,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.10-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.10-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.10 Obtener longitud de un array len()',
        task_text='❧ En otra zona se juntan gemas. Pueden ser diamantes, zafiros, rubíes, alejandritas, espinelas o amatistas. Definir un tren que lleve "diamante", "zafiro", "rubí" y "amatista". Imprimir la cantidad de gemas que se llevan y el nombre de cada una (el valor tiene que definirse mediante alguna función que devuelva la longitud del tren).',
        correct_code_text='gema0 = "diamante"\ngema1 = "zafiro"\ngema2 = "rubí"\ngema3 = "alejandrita"\ntren = [gema0,gema1,gema2,gema3]\ncantidad = len(tren)\nprint(f"El tren lleva {cantidad} gemas: {gema0}, {gema1}, {gema2}, {gema3}")',
        change_screen=change_screen,
        incorrect_code_text='gema0 = "diamante"\ntren = []\nprint(f"El tren lleva {cantidad} gemas: {gema0}")',
    )
    layout.draw()
