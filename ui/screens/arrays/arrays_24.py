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
        if output == "ELEMENTOS\ncristal azul = True\ncristal verde = False\ncantidad cristal azul = 4\ncantidad cristal verde = 0\nfuente pura = True\nfuente impura =False\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_25),
        process_input=process_input,
        level_name="arrays",
        level_number=24,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.25-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.25-w.png"),
        title_text="9. Elemento - Revisión",
        subtitle_text='9.25 Contar la cantidad de veces que aparece un valor en un array count()',
        task_text='❧ Para el último evento del año, Año Nuevo, el laboratorio necesita saber si hay suficiente cristal azul para armar una fuente. Una es pura si se arma con 4 cristales azules, si tiene menos ya se considera impura. Si es posible, reemplazar los cristales para que la fuente sea pura. El laboratorio necesita saber si hay cristal azul y verde, la cantidad de cristales de cada color, la cantidad total de cristales y si la fuente es pura o híbrida. Imprimir los datos:\nELEMENTOS\ncristal azul =\ncristal verde =\ncantidad cristal azul =\ncantidad cristal verde =\nfuente pura =\nfuente impura =',
        correct_code_text='tren = ["cristal azul", "cristal verde", "cristal azul", "cristal azul"]\ntren[1] = "cristal azul"\nhay_cristal_azul = "cristal azul" in tren\nhay_cristal_verde = "cristal verde" in tren\ncantidad_cristal_azul = tren.count("cristal azul")\ncantidad_cristal_verde = tren.count("cristal verde")\nfuente_pura = cantidad_cristal_azul == 4\nfuente_impura = cantidad_cristal_azul != 4\nprint(f"ELEMENTOS\ncristal azul = {hay_cristal_azul}\ncristal verde = {hay_cristal_verde}\ncantidad cristal azul = {cantidad_cristal_azul}\ncantidad cristal verde = {cantidad_cristal_verde}\nfuente pura = {fuente_pura}\nfuente impura ={fuente_impura}")',
        change_screen=change_screen,
        incorrect_code_text='tren = ["cristal azul", "cristal verde", "cristal azul", "cristal azul"]\nprint(f"ELEMENTOS")',
    )
    layout.draw()
