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
        if output == "En el negocio hay disponibilidad de perfume de fragancia cítrica de valor inferior a 6500: True\n":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_print()
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
        next_screen=lambda: change_screen(Screens.OPERACIONES_COMPARACION_1),
        process_input=process_input,
        level_name="operaciones_comparacion",
        level_number=0,
        module_number=6,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-6\\06-01-r.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-6\\06-01-w.png"),
        title_text="6. Operadores de Comparación",
        subtitle_text='6.1 Menor que (<)',
        task_text='  La perfumería “Essence” vende perfumes de diferentes categorías. Las categorías corresponden a:\nfragancia (floral, cítrica o especiada), temporada (verano o invierno), ocasión (día o noche) y tipo de espacio (abierto o cerrado).\nSe necesita verificar que los pedidos de los clientes estén disponibles según sus requerimientos y el stock. Completar las variables para poder realizar la venta según el pedido del cliente:\n“Estoy buscando un perfume de fragancia cítrica que cueste menos de $6500.”',
        correct_code_text='fragancia = "cítrica"\npresupuesto = 6500\nprecio = 6320\ncumple_requisitos = precio < presupuesto\nprint(f“En el negocio hay disponibilidad de perfume de fragancia {fragancia} de valor inferior a {presupuesto}: {cumple_requisitos}”)\n',
        incorrect_code_text='fragancia =\npresupuesto =\nprecio =\ncumple_requisitos =\nprint(f"En el negocio hay disponibilidad de perfume {fragancia} de valor inferior a {presupuesto}: {cumple_requisitos}")\n',
        change_screen=change_screen,
        extra_task_text='*En el caso de que no\nhayastock del perfume\nsolicitado, el stock\nserá declarado\ndirectamente como un\nvalor falso.\n\n**Los nombres de la\nfragancia, temporada,\nocasión y tipo de espacio\ndeben estar escritos\nen minúscula y de la\nmisma forma que\naparecen en la planilla.'
    )
    layout.draw()
