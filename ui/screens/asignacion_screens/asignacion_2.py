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
    input_text_with_validation = input_text + '\nprint(planeta1 == "Earth" and planeta2 == "Moon"and distancia == 384400 and diametro_planeta1 ==  12742.1 and diametro_planeta2 == 3474.8)'
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
        next_screen=lambda: change_screen(Screens.ASIGNACION_3),
        process_input=process_input,
        level_name="asignacion",
        level_number=2,
        module_number=2,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-03.png"),
        title_text="2. Asignación",
        subtitle_text='2.3 Float',
        task_text='❧ Declarar dos variables de tipo float <diametro_planeta1>\n y <diametro_planeta2 > con el diámetro de la Tierra (12742.1 km.)\n y el diámetro de la Luna (3474.8 km.).',
        correct_code_text='planeta1 = "Earth"\nplaneta2 = "Moon"\ndistancia = 384400\ndiametro_planeta1 =  12742.1\ndiametro_planeta2 = 3474.8',
        incorrect_code_text='planeta1 = "Earth"\nplaneta2 = "Moon"\ndistancia = 384400'
    )
    layout.draw()
