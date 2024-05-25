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
        r'llaves\s*=\s*\d+',
        r'llaves_estadia\s*=\s*llaves\s*-\s*\d+',
        r'llaves_comunes\s*=\s*llaves\s*-\s*\d+'
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_2),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=1,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-02-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-02-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.2 Resta (-)',
        task_text='❧  Hay que separar las llaves comunes de las llaves para estadía (rojas).\nDeclarar la variable <llaves> con la cantidad total de llaves, <llaves_estadia> y <llaves_comunes>.\nUsar la variable <llaves> en <llaves_estadia> y <llaves_comunes> para realizar una resta y que la cantidad\nde las variables coincida con la cantidad disponible de cada tipo.',
        correct_code_text='llaves = 6\nllaves_estadia = llaves -3\nllaves_comunes = llaves -3\n',
        change_screen=change_screen,
        incorrect_code_text=''
    )
    layout.draw()
