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
        if output == "En el negocio hay disponibilidad de perfume de fragancia cítrica de valor inferior a 6500: True\n":
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
        next_screen=lambda: change_screen(Screens.LANDING),
        process_input=process_input,
        level_name="arrays",
        level_number=3,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\09-03-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\09-03-w.png"),
        title_text="9. Arrays",
        subtitle_text='9.3 Crear array int a mano',
        task_text='❧ Se llegó a una zona en donde hay cristales. Se necesita saber cuántos cristales hay de cada color; la cantidad para cada color se escribe en una nota y se ubica en el carrito que corresponde. Modificar la declaración de <tren> para que almacene la cantidad de cristales en el orden: azul, transparente, naranja, verde.',
        correct_code_text='tren= [7,3,2,5]\n',
        change_screen=change_screen,
        incorrect_code_text='tren= []\n'
    )
    layout.draw()
