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
        r'llaves_diurnas\s*=\s*\d+',
        r'llaves_nocturnas\s*=\s*\d+',
    ]
    posible_pattern_1 = [
        r'llaves\s*=\s*llaves_diurnas\s*\+\s*llaves_nocturnas\s*'
    ]

    posible_pattern_2 = [
        r'llaves\s*=\s*llaves_nocturnas\s*\+\s*llaves_diurnas\s*'
    ]

    input_text = input_area.get("1.0", "end-1c")
    all_patterns_present = all(re.search(pattern, input_text) is not None for pattern in patterns)
    pattern_possible_1_present = all(re.search(pattern, input_text) is not None for pattern in posible_pattern_1)
    pattern_possible_2_present = all(re.search(pattern, input_text) is not None for pattern in posible_pattern_2)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        if all_patterns_present and (pattern_possible_1_present or pattern_possible_2_present):
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_1),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=0,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-01-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-01-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.1 Suma (+)',
        task_text='❧  En un hospedaje se usan dos tipos de llaves: llaves diurnas y llaves nocturnas.\nDeclarar dos variables, <llaves_diurnas> y <llaves_nocturnas>, para representar\n la cantidad de cada tipo de llave y sumar las variables en <llaves>.',
        correct_code_text='llaves_diurnas = 2\nllaves_nocturnas = 3\nllaves = llaves_diurnas + llaves_nocturnas\n',
        incorrect_code_text=''
    )
    layout.draw()
