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
        if output == "Cantidad total de elementos: 4\nTren: ['cristal rosa', 'cristal rosa', 'cristal rosa', 'cristal rosa']\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_15),
        process_input=process_input,
        level_name="arrays",
        level_number=14,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.15-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.15-w.png"),
        title_text="9. Array entero - Reordenamiento de array original",
        subtitle_text='9.15 Transformación de todos los valores de un array por reemplazo map()',
        task_text='❧ Se va a realizar un experimento a mayor escala para analizar el comportamiento de la estructura en los cristales. Para eso es necesario evaluar cristales del mismo tipo. Desde el laboratorio se pide que se envíen 4 cristales del mismo color, sin importar cuál sea. Mapear los cristales al color que más se repita. Imprimir la cantidad total de elementos y <tren>.',
        correct_code_text='tren = ["cristal azul", "cristal blanco", "cristal rosa", "cristal verde"]\ntren = list(map(lambda elemento: "cristal rosa", tren))\ncantidad_total = len(tren)\nprint(f"Cantidad total de elementos: {cantidad_total}\nTren: {tren}")',
        change_screen=change_screen,
        incorrect_code_text='tren = ["cristal azul", "cristal blanco", "cristal rosa", "cristal verde"]\nprint(f"Cantidad total de elementos: {cantidad_total}\nTren: ")',
    )
    layout.draw()
