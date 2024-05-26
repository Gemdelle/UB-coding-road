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
        if output == "Tren: ['rubí', 'cristal naranja', 'rubí', 'mineral impuro']\nELEMENTOS\nrubí = True\ncristal naranja = True\nmineral puro = True\ncantidad de elementos = 4\nintegral = True\nvariado = False\ntransparente = True\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_23),
        process_input=process_input,
        level_name="arrays",
        level_number=22,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.23-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.23-w.png"),
        title_text="9. Elemento - Revisión",
        subtitle_text='9.23 Determinar si un valor se encuentra en el array in',
        task_text='❧ Para Halloween se arman candelabros con las sobras de las gemas, cristales y minerales impuros, sirven solo si son rojo, naranja o negro.  En la lista que mandó el laboratorio hay que corroborar si los elementos están en el <tren> o no (si hay). Los elementos que no cumplan las características deben ser eliminados y reemplazados por algún elemento que sobre, si es que se encuentra. Además, se quiere saber cuántos elementos hay en total, si es integral (tiene todos los elementos), si es variado (tiene solo gema y mineral o solo cristal y mineral) y si es transparente (lleva al menos una gema o un cristal). Declarar una variable para determinar si existe cada elemento y para las condiciones pedidas. Imprimir la información:\nELEMENTOS\nrubí =\ncristal naranja =\nmineral puro =\ncantidad de elementos =\nintegral =\nvariado =\ntransparente =',
        correct_code_text='tren = ["rubí","cristal naranja","alejandrita","mineral impuro"]\ntren[2] = "rubí"\nhay_rubi = "rubí" in tren\nhay_cristal_naranja = "cristal naranja" in tren\nhay_mineral_puro = "mineral impuro" in tren\ncantidad_de_elementos = len(tren)\nes_integral = hay_rubi and hay_cristal_naranja  and hay_mineral_puro\nvariado = (hay_rubi and hay_mineral_puro and not hay_cristal_naranja) or (hay_rubi and hay_cristal_naranja and not hay_mineral_puro)\ntransparente = hay_rubi or hay_cristal_naranja\nprint(f"Tren: {tren}\nELEMENTOS\nrubí = {hay_rubi}\ncristal naranja = {hay_cristal_naranja}\nmineral puro = {hay_mineral_puro}\ncantidad de elementos = {cantidad_de_elementos}\nintegral = {es_integral}\nvariado = {variado}\ntransparente = {transparente}")',
        change_screen=change_screen,
        incorrect_code_text='tren = ["rubí","cristal naranja","alejandrita","mineral puro"]\nhay_rubi =\nes_integral =\nprint(f"ELEMENTOS")',
    )
    layout.draw()
