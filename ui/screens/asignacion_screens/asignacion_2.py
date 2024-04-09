import tkinter as tk
import io
import sys

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.clickable_image import ClickableImage
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def process_input(input_area, process_button, correct, incorrect):
    input_text = input_area.get("1.0", "end-1c")
    input_text_with_validation = input_text + 'print(planeta1 == "Earth" and planeta2 == "Moon"and distancia == 384400 and diametro_planeta1 =  12742.1 and diametro_planeta2 = 3474.8)'
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        exec(input_text_with_validation)

        output = captured_output.getvalue().replace("\n", "")
        if output == "True":
            process_button.grid_remove()
            repository = UserProgressRepository()
            correct()
            repository.progress_asignacion()
        else:
            incorrect()
    except Exception as e:
        incorrect()

def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    user_completed_stage = user_progress["asignacion"]["current"] > 2

    title_frame = tk.Frame(frame, bg=frame.cget('bg'))
    title_frame.grid(row=0, column=0, columnspan=8)

    title_label = WhiteStormLabel(title_frame, text=f"2. Asignación", font_size=25, foreground="#e8e8e3", bg=frame.cget('bg'))
    title_label.grid(row=0, column=1, sticky='w', padx=(0, 0), pady=(0, 0))

    subtitle_label = WhiteStormLabel(title_frame, text=f'2.3 Float', font_size=16,
                                     foreground="#e8e8e3", bg=frame.cget('bg'))
    subtitle_label.grid(row=0, column=1, sticky='w', padx=(0, 0), pady=(70, 0))

    levels_image_path = None
    for i in range(user_progress["asignacion"]["total"]):
        state = "LOCKED" if user_progress["asignacion"]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress["asignacion"]["current"] else "LOCKED" if i > user_progress["asignacion"]["current"] else "COMPLETED"
        if state == "IN_PROGRESS":
            levels_image_path = resource_path("assets\\images\\levels\\c-current.png")
        elif state == "LOCKED":
            levels_image_path = resource_path("assets\\images\\levels\\locked.png")
        elif state == "COMPLETED":
            levels_image_path = resource_path("assets\\images\\levels\\c-passed.png")
        button = ClickableImage(title_frame, image_path=levels_image_path, image_size=(60, 100), bg=frame.cget('bg'))
        button.grid(row=0, column=i + 2, sticky='w', padx=(10, 0), pady=(20, 0))

    back_arrow_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\back_arrow.png"),
                                      image_size=(87, 46), callback=lambda: change_screen(Screens.LANDING),
                                      bg=frame.cget('bg'))
    back_arrow_image.grid(row=0, column=user_progress["comentarios"]["total"] + 3, sticky='w', padx=(350, 0),
                          pady=(5, 0))

    book_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\books\\3.png"),
                                bg=frame.cget('bg'), image_size=(60, 80))
    book_image.grid(row=0, column=user_progress["comentarios"]["total"] + 3, sticky='w', padx=(470, 0), pady=(0, 0))

    code_frame = tk.Frame(frame, bg=frame.cget('bg'))
    code_frame.grid(row=1, column=0, sticky='w', padx=(40, 0), pady=(10, 0))

    task_output_frame = tk.Frame(frame, bg=frame.cget('bg'))
    task_output_frame.grid(row=1, column=1, sticky='w', padx=(40, 0), pady=(0, 0))

    task_frame = tk.Frame(task_output_frame)
    task_frame.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    task_label = WhiteStormLabel(task_frame,bg=task_frame.cget('bg'),font_size=13, width=60, height=5, text='❧ Declarar dos variables de tipo float <diametro_planeta1>\n y <diametro_planeta2 > con el diámetro de la Tierra (12742.1 km.)\n y el diámetro de la Luna (3474.8 km.).')
    task_label.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    output_frame = tk.Frame(task_output_frame, bg=frame.cget('bg'))
    output_frame.grid(row=1, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    input_area = tk.Text(code_frame, width=55, height=25, relief="ridge", borderwidth=3, font=("Courier New", 13))

    if user_completed_stage:
        input_area.insert("1.0",
                          'planeta1 = "Earth"\nplaneta2 = "Moon"\ndistancia = 384400\ndiametro_planeta1 =  12742.1\ndiametro_planeta2 = 3474.8')
    else:
        input_area.insert("1.0", 'planeta1 = "Earth"\nplaneta2 = "Moon"\ndistancia = 384400')

    input_area.grid(row=0, column=0, sticky='w')

    if user_completed_stage:
        correct_music_sheet(output_frame, code_frame, change_screen, input_area)
    else:
        incorrect_music_sheet(output_frame)

    if not user_completed_stage:
        process_button = tk.Button(code_frame,width=7, height=2, text="Run", command=lambda: process_input(input_area, process_button,
                                                                                         lambda: correct_music_sheet(
                                                                                             output_frame, code_frame, change_screen, input_area),
                                                                                         lambda: incorrect_music_sheet(
                                                                                             output_frame)))
        process_button.grid(row=1, column=0, sticky='e', padx=(0, 0), pady=(10, 10))
        process_input(input_area,process_button,lambda: correct_music_sheet(output_frame, code_frame, change_screen, input_area), lambda: incorrect_music_sheet(output_frame))
    else:
        empty_frame = tk.Frame(code_frame,width=1, height=60, bg=frame.cget('bg'))
        empty_frame.grid(row=1, column=0, sticky='e', padx=(0, 0), pady=(0, 0))
        input_area.config(state=tk.DISABLED, cursor="arrow")

def incorrect_music_sheet(output_frame):
    output_image1 = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-3\\earth.png"),
                                   image_size=(142, 225), bg=output_frame.cget('bg'))
    output_image1.grid(row=0, column=0, sticky='w', padx=(100, 0), pady=(130, 100))
    output_image2 = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-3\\moon.png"),
                                   image_size=(142, 225), bg=output_frame.cget('bg'))
    output_image2.grid(row=0, column=0, sticky='w', padx=(330, 0), pady=(130, 100))

def correct_music_sheet(output_frame, code_frame, change_screen, input_area):
    output_image1 = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-3\\earth.png"),
                                   image_size=(142, 225), bg=output_frame.cget('bg'))
    output_image1.grid(row=0, column=0, sticky='w', padx=(50, 0), pady=(130, 100))
    output_image2 = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-3\\moon.png"),
                                   image_size=(142, 225), bg=output_frame.cget('bg'))
    output_image2.grid(row=0, column=0, sticky='w', padx=(430, 0), pady=(130, 100))
    next_level_button = tk.Button(code_frame, width=7, height=2, text="Next",
                                  command=lambda: change_screen(Screens.ASIGNACION_3))
    next_level_button.grid(row=1, column=0, sticky='e', padx=(0, 0), pady=(10, 10))
    pet_image = ClickableImage(code_frame, image_path=resource_path("assets\\images\\pet.png"),
                               image_size=(100, 50), bg=code_frame.cget('bg'))
    pet_image.grid(row=1, column=0, sticky='e', padx=(0, 75), pady=(10, 10))
    input_area.config(state=tk.DISABLED, cursor="arrow")
