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
        if output == "[3, 2.5, 2, 1.5]\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_6),
        process_input=process_input,
        level_name="arrays",
        level_number=5,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.6-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.6-w.png"),
        title_text="9. Arrays - Creación",
        subtitle_text='9.6 Crear array int con variables',
        task_text='❧ Los cristales pueden estar enteros o partidos, en el caso de estar enteros el valor es de 1, pero si están partidos, el valor corresponde a 0.5. Modificar la declaración de <tren> para que almacene la cantidad de cristales en el orden que corresponde: azul, transparente, naranja, verde.',
        correct_code_text='cristales_rosas = 3\ncristales_azules = 2.5\ncristales_blancos = 1.5\ncristales_violetas = 2\ntren = [cristales_rosas, cristales_azules, cristales_blancos, cristales_violetas]',
        change_screen=change_screen,
        incorrect_code_text='cristales_rosas = 3\n'
    )
    layout.draw()
