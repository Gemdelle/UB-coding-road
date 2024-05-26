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
        if output == "El tren tiene las siguientes gemas: ['amatista', 'diamante', 'rubí', 'zafiro']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_11),
        process_input=process_input,
        level_name="arrays",
        level_number=10,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.11-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.11-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.11 Ordenar un array sort()',
        task_text='❧ Para registrar las gemas es necesario que estén en orden alfabético; además, hubo una confusión y en lugar de extraer un amatista se extrajeron dos rubíes. Reemplazar el primer rubí por amatista (mediante la notación de arrays) y ordenarlas alfabéticamente.',
        correct_code_text='tren = [ "diamante", "rubí", "rubí", "zafiro"]\ntren[1] = "amatista"\ntren.sort()\nprint(f"El tren tiene las siguientes gemas: {tren}")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "diamante", "rubí", "rubí", "zafiro"]\nprint(f"El tren tiene las siguientes gemas: {tren}")',
    )
    layout.draw()
