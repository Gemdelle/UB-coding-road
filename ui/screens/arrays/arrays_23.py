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
        if output == "ELEMENTOS\nrubí = True\ncristal naranja = False\ncristal verde = True\narmar árbol = True\narmar árbol barato = True\narmar árbol caro = False\n":
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
        next_screen=lambda: change_screen(Screens.ARRAYS_24),
        process_input=process_input,
        level_name="arrays",
        level_number=23,
        module_number=9,
        background_image_path=resource_path("assets\\images\\background.png"),
        correct_output_image_path=resource_path("assets\\images\\ex-9\\9.24-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-9\\9.24-w.png"),
        title_text="9. Elemento - Revisión",
        subtitle_text='9.24 Determinar si un valor se encuentra en el array in',
        task_text='❧ Para Navidad se hacen adornos con rubíes y una estrella con cristal verde o cristal naranja. Las estrellas naranjas son más caras que las verdes y sirven para hacer árboles caros. Hubo un accidente y se cayeron algunas cosas del tren…Cargar las gemas y cristales que corresponden y, en el caso que haya, eliminar los elementos que no se necesitan. Se necesita que los cristales estén primero y los rubíes al final, y con un rubí y un cristal ya alcanza para armar un árbol. El laboratorio necesita saber si está cada uno de los elementos, si alcanzan para armar aunque sea un árbol (ya sea caro o barato), si se puede armar un árbol caro y si se puede armar un árbol barato. Imprimir los datos de la lista para el laboratorio con el formato:\nELEMENTOS\nrubí =\ncristal naranja =\ncristal verde =\narmar árbol =\narmar árbol barato =\narmar árbol caro =',
        correct_code_text='tren = ["amatista","espinela"]\ntren.clear()\ntren.append("cristal verde")\ntren.append("rubí")\ntren.append("rubí")\ntren.append("rubí")\nhay_rubi = "rubí" in tren\nhay_cristal_naranja = "cristal naranja" in tren\nhay_cristal_verde = "cristal verde" in tren\narmar_arbol = (hay_cristal_naranja or hay_cristal_verde) and hay_rubi\narmar_arbol_barato = hay_cristal_verde and hay_rubi\narmar_arbol_caro = hay_cristal_naranja and hay_rubi\nprint(f"ELEMENTOS\nrubí = {hay_rubi }\ncristal naranja = {hay_cristal_naranja }\ncristal verde = {hay_cristal_verde}\narmar árbol = {armar_arbol}\narmar árbol barato = {armar_arbol_barato}\narmar árbol caro = {armar_arbol_caro}")',
        change_screen=change_screen,
        incorrect_code_text='tren = ["amatista","espinela"]\nprint(f"ELEMENTOS")',
    )
    layout.draw()
