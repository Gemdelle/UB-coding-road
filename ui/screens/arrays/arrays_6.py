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
        if output == "En el primer lugar hay un mineral opaco y en el segundo un mineral opaco\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_7),
        process_input=process_input,
        level_name="arrays",
        level_number=6,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.7-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.7-w.png"),
        title_text="9. Arrays - Acceso y modificación manual",
        subtitle_text='9.7 Acceder a las posiciones de un array con print I',
        task_text='❧ El tren <tren> actual lleva minerales opacos y brillantes. Imprimir el tipo de mineral que hay en el primer y segundo lugar.',
        correct_code_text='tren = [ "opaco", "opaco", "brillante", "opaco"]\nmineral = tren[0]\nmineral2 = tren[1]\nprint(f"En el primer lugar hay un mineral {mineral} y en el segundo un mineral {mineral2}")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "opaco", "opaco", "brillante", "opaco"]\nmineral2 = tren[1]\nprint(f"En el primer lugar hay un mineral {mineral} y en el segundo un mineral {mineral2}")',
        extra_task_text='*Analizar en qué posición\nde la lista se encuentra\nla gema que se pide\nimprimir y acceder con\nla notación tren[n°].'
    )
    layout.draw()
