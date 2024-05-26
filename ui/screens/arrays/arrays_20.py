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
        if output == "Tren: ['diamante', 'cristal verde', 'rubí', 'zafiro']\nEl tren está lleno: True\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_21),
        process_input=process_input,
        level_name="arrays",
        level_number=20,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.21-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.21-w.png"),
        title_text="9. Elemento - Modificación",
        subtitle_text='9.21 Agregar un elemento en la posición especificada insert()',
        task_text='❧ Para procesar los elementos más rápido, el laboratorio exige que se entreguen ordenados por color, del más claro a más oscuro. En el <tren> actual se lleva un diamante, una alejandrita y un zafiro, pero el encargado se olvidó de agregar un rubí. El ordenamiento de colores que pasó el laboratorio corresponde a: blanco, rosa, verde, rosa, rojo, violeta, azul. Además, últimamente hay un problema para procesar las gemas verdes, en el caso de que se corresponda con algún elemento del tren, debe ser reemplazado por un cristal de ese color. Insertar el rubí en el <tren> en el lugar que corresponda e imprimir el estado del tren, si está lleno o no.',
        correct_code_text='tren = ["diamante","alejandrita","zafiro"]\ntren.insert(2,"rubí")\ntren[1] = "cristal verde"\nesta_lleno = len(tren) == 4\nprint(f"El tren está lleno: {esta_lleno}\nprint(f"Tren: {tren}\nEl tren está lleno: {esta_lleno}")',
        change_screen=change_screen,
        incorrect_code_text='tren = ["diamante","alejandrita","zafiro"]\nprint(f"Tren: {tren}\nEl tren está lleno: {esta_lleno}")',
    )
    layout.draw()
