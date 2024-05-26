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
        if output == "ELEMENTOS\ncristal azul = 1\nespinela = 0\nmineral impuro = 2\ncristal naranja = 3\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_22),
        process_input=process_input,
        level_name="arrays",
        level_number=21,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.22-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.22-w.png"),
        title_text="9. Elemento - Revisión",
        subtitle_text='9.22 Devolver el índice de un valor (primera aparición) index()',
        task_text='❧ Para agilizar el análisis, el laboratorio empezó a enviar planillas en las que hay que definir la posición del tren que ocupa cada elemento de la lista. El formato de la lista enviada es:\nELEMENTOS\ncristal azul =\nespinela =\nmineral impuro =\ncristal naranja =\nGuardar la posición (índice) de cada elemento en una variable y definir la impresión para que sea igual a la enviada por el laboratorio.',
        correct_code_text='tren = ["espinela", "cristal azul", "mineral impuro", "cristal naranja"]\nindex_espinela = tren.index("espinela")\nindex_cristal_azul = tren.index("cristal azul")\nindex_mineral_impuro = tren.index("mineral impuro")\nindex_cristal_naranja = tren.index("cristal naranja")\nprint(f"ELEMENTOS\ncristal azul = {index_cristal_azul}\nespinela = {index_espinela }\nmineral impuro = {index_mineral_impuro}\ncristal naranja = {index_cristal_naranja}")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "espinela", "cristal azul", "mineral impuro", "cristal naranja"]\nindex_espinela =\nprint(f"ELEMENTOS")',
    )
    layout.draw()
