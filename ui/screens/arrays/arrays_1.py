import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound

def process_input(input_area, process_button, code_canvas, correct, incorrect):
    input_text = input_area.get("1.0", "end-1c")
    input_text_with_validation = input_text + '\nprint(carrito)'
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(input_text_with_validation)

        output = captured_output.getvalue()
        if output == "['carrito 0', 'carrito 1', 'carrito 2', 'carrito 3']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_2),
        process_input=process_input,
        level_name="arrays",
        level_number=1,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.2-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.2-w.png"),
        title_text="9. Arrays - Modificación",
        subtitle_text='9.2 Modificar array string con variables',
        task_text='❧ El arreglo <tren> contiene tres carritos (recordar que el primero elemento corresponde al índice 0 de la lista). Declarar la variable <carrito3> y agregarla al tren para que el tren esté formado por cuatro carritos en total.',
        correct_code_text='carrito0 = "carrito 0"\ncarrito1 = "carrito 1"\ncarrito2 = "carrito 2"\ncarrito3 = "carrito 3"\ncarrito = [carrito0,carrito1,carrito2,carrito3]\n',
        change_screen=change_screen,
        incorrect_code_text='carrito0 = "carrito 0"\ncarrito1 = "carrito 1"\ncarrito2 = "carrito 2"\ncarrito = [carrito0,carrito1,carrito2]\n'
    )
    layout.draw()
