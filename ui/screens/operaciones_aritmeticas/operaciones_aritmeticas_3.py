import tkinter as tk
import io
import sys
import re

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound


def process_input(input_area, process_button, code_canvas, correct, incorrect):
    patterns = [
        r'llaves_estadia_corta\s*=\s*\d+',
        r'llaves_estadia_larga\s*=\s*\d+',
        r'personas_estadia_corta\s*=\s*\d+',
        r'personas_estadia_larga\s*=\s*\d+',
        r'personas_habitacion_corta\s*=\s*personas_estadia_corta\s*/\s*llaves_estadia_corta',
        r'personas_habitacion_larga\s*=\s*personas_estadia_larga\s*/\s*llaves_estadia_larga'
    ]

    input_text = input_area.get("1.0", "end-1c")
    all_patterns_present = all(re.search(pattern, input_text) is not None for pattern in patterns)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        if all_patterns_present:
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_input()
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_4),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=3,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-03-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-03-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.4 División entera con variables (//)',
        task_text='❧  Además, las llaves se dividen según el tiempo de estadía: celestes para estadías cortas\ny rosas para estadías largas. Se espera que cada habitación tenga\nla misma cantidad de huéspedes. Hay 10 personas para estadías cortas y 12\npersonas para estadías largas. Declarar las variables <personas_estadia_corta> y  <personas_estadia_larga>\ncon el valor correspondiente. Declarar <personas_haitacion_corta> y <personas_habitacion_larga>, efectuar\nuna división con las variables de estadía declaradas y <llaves_estadia_corta> y <llaves_estadia_larga>\npara asignar la cantidad correspondiente de personas por habitación a cada tipo de llave.',
        correct_code_text='llaves_estadia_corta = 2\nllaves_estadia_larga = 3\npersonas_estadia_corta = 10\npersonas_estadia_larga = 12\npersonas_habitacion_corta = personas_estadia_corta / llaves_estadia_corta\npersonas_habitacion_larga = personas_estadia_larga / llaves_estadia_larga\n',
        change_screen=change_screen,
        incorrect_code_text='llaves_estadia_corta = 2\nllaves_estadia_larga = 3\n'
    )

    layout.draw()
