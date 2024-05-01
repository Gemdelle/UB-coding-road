import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound


def process_input(input_area, process_button, code_canvas, correct, incorrect):
    input_text = input_area.get("1.0", "end-1c")
    input_text_with_validation = input_text + '\nprint(isinstance(numero, str))'
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        exec(input_text_with_validation)

        output = captured_output.getvalue().replace("\n", "")
        if output == "True":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_transformacion()
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
        next_screen=lambda: change_screen(Screens.TRANSFORMACION_3),
        process_input=process_input,
        level_name="transformacion",
        level_number=2,
        module_number=3,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-4\\4-3-str.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-4\\4-3-int.png"),
        title_text="3. Transformación de Tipo",
        subtitle_text='3.3 int a str',
        task_text='❧ Transformar el valor 42\nalmacenado en <numero> de entero a string.',
        correct_code_text='numero = str(42)',
        change_screen=change_screen,
        incorrect_code_text='numero = 42\n'
    )
    layout.draw()