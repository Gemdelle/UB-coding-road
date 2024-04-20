import io
import sys
import tkinter as tk

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
    input_text = input_area.get("1.0", "end-1c")
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(input_text)

        output = captured_output.getvalue()
        if output == "Please\nClimb\nthe\ntower\nfast\n":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_print()
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
        level_name="print",
        level_number=6,
        module_number=1,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-2\\3.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-2\\1.png"),
        title_text="1. Print",
        subtitle_text='1.6 String formateado y salto de línea',
        task_text='❧ Imprimir la frase "Please climb the tower fast" con una\npalabra en cada renglón utilizando un string\nformateado con y saltos de línea.',
        correct_code_text='palabra1 = "palabra1 = "Climb"\npalabra2 = "the"\npalabra3 = "tower"\nprint(f"Please\n{palabra1}\n{palabra2}\n{palabra3}\nfast")',
        incorrect_code_text='palabra1 = "Climb"\npalabra2 = "the"\npalabra3 = "tower"'
    )
    layout.draw()
