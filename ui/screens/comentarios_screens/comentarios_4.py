import tkinter as tk
import re

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.set_time_out_manager import SetTimeoutManager
from utils.sound_manager import play_correct_sound, play_wrong_sound


def showWrongMessage(code_frame):
    # TODO: Replace message with png word
    error_message_canvas = tk.Canvas(code_frame, width=100, height=30)
    error_message_canvas.create_text(0, 15, text="Try again", fill="#7A0D13", font=("Georgia", 16, "bold"), anchor="w")
    wrong_message_id = code_frame.create_window(500, 620, window=error_message_canvas, anchor="w")
    set_timeout_manager = SetTimeoutManager()
    set_timeout_manager.setTimeout(lambda: code_frame.delete(wrong_message_id), 2)
def process_input(input_area, process_button, code_canvas, correct, incorrect):
    global comentarios_0_completed
    input_text = input_area.get("1.0", "end-1c")

    try:
        matches = re.findall(r'"""[^"""]+"""', input_text)
        if len(matches) > 0:
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_comentarios()
            play_correct_sound()
        else:
            incorrect()
            play_wrong_sound()
            showWrongMessage(code_canvas)
    except Exception as e:
        incorrect()
        play_wrong_sound()
        showWrongMessage(code_canvas)

def draw(frame, change_screen):
    layout = ScreenLayout(
        frame=frame,
        back_screen=lambda: change_screen(Screens.LANDING),
        next_screen=lambda: change_screen(Screens.LANDING),
        process_input=process_input,
        level_name="comentarios",
        level_number=4,
        module_number=0,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-1\\2.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-1\\4.png"),
        title_text="0. Comentarios",
        subtitle_text='0.5 Agregar un comentario """ entre prints',
        task_text='❧ Se quiere agregar un comentario sobre la música\n al principio del código, pero sin que aparezca en la partitura.\n Escribir un comentario (Buena, muy triste, mala, etc.)\nantes de la declaración de las variables.',
        correct_code_text='"""\nBuena\n"""\nautor = "Ludwig van Beethoven"\nprint(autor)\ntitulo = "Sonata para piano No. 14"\nprint(titulo)\npartitura = True\nprint(partitura)',
        incorrect_code_text='autor = "Ludwig van Beethoven"\nprint(autor)\ntitulo = "Sonata para piano No. 14"\nprint(titulo)\npartitura = True\nprint(partitura)'
    )
    layout.draw()
