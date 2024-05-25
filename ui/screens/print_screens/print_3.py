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

        output = captured_output.getvalue().replace("\n", "")
        if output == "Climb the tower":
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
        next_screen=lambda: change_screen(Screens.PRINT_4),
        process_input=process_input,
        level_name="print",
        level_number=3,
        module_number=1,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-2\\2.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-2\\1.png"),
        title_text="1. Print",
        subtitle_text='1.3. Coma → print(word,word)',
        task_text='❧ Imprimir nuevamente “Climb the tower”,\npero esta vez a modo de frase y utilizando “,”.',
        correct_code_text='palabra1 = "Climb"\npalabra2 = "the"\npalabra3 = "tower"\nprint(palabra1, palabra2, palabra3)',
        change_screen=change_screen,
        incorrect_code_text='palabra1 = "Climb"\npalabra2 = "the"\npalabra3 = "tower"'
    )
    layout.draw()
