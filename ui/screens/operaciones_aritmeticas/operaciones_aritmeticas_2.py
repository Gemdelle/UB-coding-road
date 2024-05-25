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
        r'saldo\s*=\s*\d+\.\d+',
        r'precio_noche\s*=\s*\d+\.\d+',
        r'cantidad_dias_posibles\s*=\s*int\(\s*saldo\s*/\s*precio_noche\s*\)',
        r'precio_final\s*=\s*cantidad_dias_posibles\s*\*\s*precio_noche',
        r'llave\s*=\s*\"[^\"]*\"'
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_3),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=2,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-5\\05-02-right.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-5\\05-02-wrong.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.3 División con variables (/)',
        task_text='❧  Un cliente quiere averiguar cuántos días puede alojarse con $12000. Calcular para cuántos días\nle alcanza y cuánto le saldría en total si la noche está $2600.8. Si le alcanza para más de 3 noches, le corresponde\nla llave “grande”; sino, la llave “chica”. Declarar las variables <saldo> (float), <precio_noche> (float),\n<cantidad_dias_posibles> (int), <precio_final> (float) y <llave> (str). Imprimir el mensaje “Con {x} dinero\nse puede alojar {y} días. Corresponde llave {z}”.',
        correct_code_text='saldo = 12000.0\nprecio_noche = 2600.8\ncantidad_dias_posibles = int(saldo / precio_noche)\nprecio_final = cantidad_dias_posibles * precio_noche\nllave = "grande"\n',
        change_screen=change_screen,
        incorrect_code_text=''
    )
    layout.draw()
