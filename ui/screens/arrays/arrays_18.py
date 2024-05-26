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
        if output == "El tren tiene las gemas: ['cristal verde', 'cristal verde', 'cristal verde', 'alejandrita']\nEn el último lugar se lleva alejandrita: True\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_19),
        process_input=process_input,
        level_name="arrays",
        level_number=18,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.19-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.19-w.png"),
        title_text="9. Elemento - Modificación",
        subtitle_text='9.19 Eliminar el último elemento de un array pop()',
        task_text='❧ Para San Patricio se juntan cristales verdes y alejandritas (poco comunes). Hubo un error en la carga y se agregaron elementos de otro color. Como las alejandritas no se encuentran seguido, es importante saber si en el último lugar se encontró una. Eliminar los elementos que no corresponden, agregar un cristal verde y una alejandrita (declaradas como <cristal> y <gema>) e imprimir si en el último lugar se lleva una alejandrita.',
        correct_code_text='# gema verde: alejandrita\ntren = [ "cristal verde", "cristal verde", "diamante", "zafiro"]\ntren.pop()\ntren.pop()\ncristal = "cristal verde"\ngema = "alejandrita"\ntren.append(cristal)\ntren.append(gema)\nhay_alejandrita = tren[len(tren)-1] == "alejandrita"\nprint(f"El tren tiene las gemas: {tren}\nEn el último lugar se lleva alejandrita: {hay_alejandrita}")',
        change_screen=change_screen,
        incorrect_code_text='# gema verde: alejandrita\ntren = [ "cristal verde", "cristal verde, "diamante", "zafiro"]\n# eliminar elementos que no son verdes\n# declarar <cristal> y <gema>\n# agregar <cristal> y <gema> a <tren>\n# declarar <hay_alejandrita>\nprint(f"El tren tiene las gemas: {tren}\nEn el último lugar se lleva alejandrita: {hay_alejandrita}")',
    )
    layout.draw()
