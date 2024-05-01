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
        if output == "En el negocio hay disponibilidad de perfume de fragancia cítrica de valor inferior a 6500: True\n":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_print()
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
        next_screen=lambda: change_screen(Screens.ARRAYS_3),
        process_input=process_input,
        level_name="arrays",
        level_number=2,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\09-02-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\09-02-w.png"),
        title_text="9. Arrays",
        subtitle_text='9.2 Crear array string a mano',
        task_text='❧ Ya se crearon arreglos que contienen valores ingresados a mano en su declaración (ejercicio 8.0) y arreglos que almacenan variables (ejercicio 8.1). Ahora que ya se sabe crear arreglos, modificar tren <tren> para que desde su declaración contenga “cristal”, “mineral” y “gema”',
        correct_code_text='tren = [ "cristal", "mineral", "gema"]\n',
        incorrect_code_text='tren = []\n',
        change_screen=change_screen,
        extra_task_text='*Los elementos aparecerán\ndirectamente en carritos\nya que el carrito es el\ncontenedor del elemento,\nla POSICIÓN que ocupa\nel elemento en la lista.\nEl elemento es el VALOR\nalmacenado en esa\nposición, y puede ser\ncualquiera, “gema”,\n“cristal”, etc.'
    )
    layout.draw()
