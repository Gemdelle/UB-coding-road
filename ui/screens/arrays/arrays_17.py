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
        if output == "El tren tiene: ['cristal rosa', 'gema rosa', 'gema roja', 'mineral rosa']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_18),
        process_input=process_input,
        level_name="arrays",
        level_number=17,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.18-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.18-w.png"),
        title_text="9. Elemento - Modificación",
        subtitle_text='9.18 Agregar un elemento al final de un array append()',
        task_text='❧ Para San Valentín se juntan cristales, gemas y minerales rojos y rosas. Primero se cargan todos los cristales, después las gemas, y por último los minerales, y a su vez, se carga primero rosa y después rojo. Declarar un <tren> y una variable para cada lugar (elemento + color) y después cargar el <tren>.',
        correct_code_text='lugar0 = "cristal rosa"\nlugar1 = "gema rosa"\nlugar2 = "gema roja"\nlugar3 = "mineral rosa"\ntren = [lugar0, lugar1, lugar2, lugar3]\nprint(f"El tren tiene: {tren}")',
        change_screen=change_screen,
        incorrect_code_text='# gema rosa: espinela\n# gema roja: rubí\nlugar0 = "cristal rosa"\ntren = []\nprint(f"El tren tiene: {tren}")',
        extra_task_text="*El método necesario para\nsumar elementos a un\narray es el append."
    )
    layout.draw()
