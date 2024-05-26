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
        if output == "El tren lleva 1 minerales opacos y 3 minerales brillantes\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_9),
        process_input=process_input,
        level_name="arrays",
        level_number=8,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.9-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.9-w.png"),
        title_text="9. Arrays - Acceso y modificación manual",
        subtitle_text='9.9 Sobreescribir un valor',
        task_text='❧ El <tren> actual lleva minerales opacos y brillantes, pero se necesita reemplazar cada uno por el otro tipo. Cambiar los minerales opacos por brillantes, y los brillantes por opacos. También se necesita saber cuántos hay de cada tipo, contar cuántos minerales de cada tipo van a quedar y almacenar los valores en <opacos> y <brillantes>.',
        correct_code_text='tren = [ "brillante", "opaco", "opaco", "opaco"]\ntren[0] = "opaco"\ntren[1] = "brillante"\ntren[2] = "brillante"\ntren[3] = "brillante"\nopacos = 1\nbrillantes = 3\nprint(f"El tren lleva {opacos} minerales opacos y {brillantes} minerales brillantes")',
        change_screen=change_screen,
        incorrect_code_text='tren = [ "brillante", "opaco", "opaco", "opaco"]\nprint(f"El tren lleva {opacos} minerales opacos y {brillantes} minerales brillantes")',
    )
    layout.draw()
