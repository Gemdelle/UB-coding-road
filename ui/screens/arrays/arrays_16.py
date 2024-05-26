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
        if output == "2\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_17),
        process_input=process_input,
        level_name="arrays",
        level_number=16,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.17-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.17-w.png"),
        title_text="9. Nuevo Array - Mutación de longitud",
        subtitle_text='9.17 Filtrar un array en base a una condición filter() y list()',
        task_text='❧ Se quiere realizar el mismo estudio para los minerales, específicamente los impuros, ya que tienen otra estructura. Anteriormente se reemplazaron todos los elementos por otro elemento; en este caso se necesita reemplazar únicamente los minerales puros por los minerales impuros, es decir, se reemplazan solo si son puros. Imprimir <tren>.',
        correct_code_text='tren = ["mineral impuro", "cristal blanco", "cristal blanco", "mineral impuro"]\ntren_filtrado = list(filter(lambda elemento: elemento == "mineral impuro", tren))\ncantidad_de_mineral_impuro = len(tren_filtrado)\nprint(cantidad_de_mineral_impuro)',
        change_screen=change_screen,
        incorrect_code_text='tren = ["mineral impuro", "cristal blanco", "cristal blanco", "mineral impuro"]',
    )
    layout.draw()
