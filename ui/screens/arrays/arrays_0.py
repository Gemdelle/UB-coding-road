import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound

def process_input(input_area, process_button, code_canvas, correct, incorrect):
    input_text = input_area.get("1.0", "end-1c")
    input_text_with_validation = input_text + '\nprint(tren)'
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(input_text_with_validation)

        output = captured_output.getvalue()
        if output == "['carrito 0', 'carrito 1', 'carrito 2']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_1),
        process_input=process_input,
        level_name="arrays",
        level_number=0,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.1-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.1-w.png"),
        title_text="9. Arrays - Modificación",
        subtitle_text='9.1 Modificar array string a mano',
        task_text='❧ Un trabajador de una mina necesita mover elementos (cristales, minerales y gemas). Cada elemento se guarda en un carrito, y una sucesión de carritos forma un tren. Cada carrito va a representar la posición de ese elemento en el tren. El tren declarado es un arreglo (array) que contiene un elemento ("carrito viejo"). Modificar el arreglo para que contenga cuatro carritos con la palabra carrito y su posición dentro del tren, por ejemplo: "carrito 0", "carrito 5". El primer carrito debe ser el número 0.',
        correct_code_text='tren = ["carrito 0", "carrito 1", "carrito 2"]\n',
        change_screen = change_screen,
        incorrect_code_text='tren = ["carrito viejo"]\n'
    )
    layout.draw()
