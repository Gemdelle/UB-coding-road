import tkinter as tk
import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound

def process_input(input_area, process_button, code_canvas, correct, incorrect):
    input_text = input_area.get("1.0", "end-1c")
    input_text_with_validation = input_text + '\nprint(planeta1 == "Venus" and planeta2 == "Mercury")'
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        exec(input_text_with_validation)

        output = captured_output.getvalue().replace("\n", "")
        if output == "True":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_asignacion()
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
        next_screen=lambda: change_screen(Screens.ASIGNACION_5),
        process_input=process_input,
        level_name="asignacion",
        level_number=4,
        module_number=2,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-05.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        title_text="2. Asignación",
        subtitle_text='2.5 Sobreescribir variables de tipo string',
        task_text='❧ Sobreescribir las variables <planeta1> y <planeta2>\npara que en lugar de “Earth” y “Moon”\nguarden el valor “Venus” y “Mercury”.',
        correct_code_text='planeta1 = "Venus"\nplaneta2 = "Mercury"',
        change_screen=change_screen,
        incorrect_code_text='planeta1 = "Earth"\nplaneta2 = "Moon"\n'
    )
    layout.draw()

