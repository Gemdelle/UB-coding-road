import tkinter as tk
import io
import sys

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
        if output == "Personas a hospedar en habitaciones grandes: 18\nPersonas a hospedar en habitaciones chicas: 15\nTotal personas a hospedar: 33\n":
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_ARITMETICAS_5),
        process_input=process_input,
        level_name="operaciones_aritmeticas",
        level_number=4,
        module_number=5,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-3\\02-01.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-3\\02-02.png"),
        title_text="5. Operaciones Aritméticas",
        subtitle_text='5.5 Multiplicación con variables (*)',
        task_text='❧  Un grupo de personas quiere hospedarse. Hay 8 habitaciones disponibles: 3 llaves\ncorresponden a habitaciones para 6 personas, las restantes (que no se entregaron todavía, en color oscuro)\ncorresponden a habitaciones para 3 personas. Declarar las variables <llaves_hab_chicas>\ny <llaves_hab_grandes> con la cantidad de llaves para cada tipo de habitación según la imagen.\nDeclarar <capacidad_hab_chicas> y <capacidad_hab_chicas> con la capacidad de cada tipo de habitación.\nDeclarar también <personas_hab_chicas> y <personas_hab_grandes>, realizar la multiplicación\ncorrespondiente para almacenar la cantidad de personas totales en cada tipo de habitación.',
        correct_code_text='llaves_hab_grandes = 3\nllaves_hab_chicas = 5\ncapacidad_hab_grandes = 6\ncapacidad_hab_chicas = 3\npersonas_hab_grandes = llaves_hab_grandes * capacidad_hab_grandes\npersonas_hab_chicas = llaves_hab_chicas * capacidad_hab_chicas\nprint("Personas a hospedar en habitaciones grandes:", personas_hab_grandes)\nprint("Personas a hospedar en habitaciones chicas:", personas_hab_chicas)\nprint("Total personas a hospedar:", personas_hab_grandes + personas_hab_chicas)\n',
        incorrect_code_text=''
    )

    layout.draw()
