import io
import sys
from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.screen_layout import ScreenLayout
from utils.resource_path_util import resource_path
from utils.sound_manager import play_correct_sound, play_wrong_sound

def process_input(input_area, process_button, code_canvas, correct, incorrect):
    global comentarios_0_completed
    input_text = input_area.get("1.0", "end-1c")
    captured_output = io.StringIO()
    sys.stdout = captured_output

    try:
        exec(input_text)

        output = captured_output.getvalue().replace("\n", "")
        if output == "Sonata para piano No. 14":
            code_canvas.delete(process_button)
            repository = UserProgressRepository()
            correct()
            repository.progress_comentarios()
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
        next_screen=lambda: change_screen(Screens.COMENTARIOS_2),
        process_input=process_input,
        level_name="comentarios",
        level_number=1,
        module_number=0,
        background_image_path=resource_path("assets\\images\\background.jpg"),
        correct_output_image_path=resource_path("assets\\images\\ex-1\\2.png"),
        incorrect_output_image_path=resource_path("assets\\images\\ex-1\\1a.png"),
        title_text="0. Comentarios",
        subtitle_text="0.2 Descomentar una variable con #",
        task_text='❧ Descomentar la variable "titulo" y la línea que la imprime,\nque está actualmente comentada con el símbolo #,\npara que se tenga en cuenta en la ejecución del programa.',
        correct_code_text='titulo = "Sonata para piano No. 14"\nprint(titulo)',
        incorrect_code_text='#titulo = "Sonata para piano No. 14"\n#print(titulo)'
    )
    layout.draw()

