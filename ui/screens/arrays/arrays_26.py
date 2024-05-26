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
        if output == " cristalnaranja cristalblanco cristalverde cristalrosa \n":
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
        next_screen=lambda: change_screen(Screens.LANDING),
        process_input=process_input,
        level_name="arrays",
        level_number=26,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.27-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.27-w.png"),
        title_text="9. Transformación - String y Array",
        subtitle_text='9.27 Definir un array en base a la separación de un string mediante un valor (caracter/es) split()',
        task_text='❧ Como se están juntando los elementos demasiado rápido, desde el laboratorio se decidió enviar el mensaje encriptado. Encima, la nota se deshizo por la lluvia y en el intento de arreglarla, un minero la pegó al revés. Se pide desencriptar el mensaje y reordenarlo para no confundir el orden en el que hay que ubicar lo que se pide. Imprimir <mensaje_final>.',
        correct_code_text='mensaje = "cristalescristalrosacristalescristalverdecristalescristalblancocristalescristalnaranjacristales"\ntren = []\nmensaje_final = mensaje.split("cristales")\nmensaje_final.reverse()\nmensaje_final = " ".join(mensaje_final)\nprint(mensaje_final)',
        change_screen=change_screen,
        incorrect_code_text='mensaje = "cristalescristalrosacristalescristalverdecristalescristalblancocristalescristalnaranjacristales"\ntren = []',
    )
    layout.draw()
