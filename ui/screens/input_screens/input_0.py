import tkinter as tk
import io
import sys
import re

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.clickable_image import ClickableImage
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def process_input(input_area, process_button, correct, incorrect):
    patterns = [
        r'direccion\s*=\s*',
        r'input\(',
        r'print\('
    ]

    input_text = input_area.get("1.0", "end-1c")
    # Check if all patterns are present
    all_patterns_present = all(re.search(pattern, input_text) is not None for pattern in patterns)
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        if all_patterns_present:
            process_button.grid_remove()
            repository = UserProgressRepository()
            correct()
            repository.progress_input()
        else:
            incorrect()
    except Exception as e:
        incorrect()

def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    user_completed_stage = user_progress["input"]["current"] > 0

    title_frame = tk.Frame(frame, bg=frame.cget('bg'))
    title_frame.grid(row=0, column=0, columnspan=8)

    title_label = WhiteStormLabel(title_frame, text=f"4. Input", font_size=25, foreground="#e8e8e3", bg=frame.cget('bg'))
    title_label.grid(row=0, column=1, sticky='w', padx=(0, 0), pady=(0, 0))

    subtitle_label = WhiteStormLabel(title_frame, text=f'4.1 Ingresar un texto y printearlo', font_size=16,
                                     foreground="#e8e8e3", bg=frame.cget('bg'))
    subtitle_label.grid(row=0, column=1, sticky='w', padx=(40, 0), pady=(70, 0))

    levels_image_path = None
    for i in range(user_progress["input"]["total"]):
        state = "LOCKED" if user_progress["input"]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress["input"]["current"] else "LOCKED" if i > user_progress["input"]["current"] else "COMPLETED"
        if state == "IN_PROGRESS":
            levels_image_path = resource_path("assets\\images\\levels\\e-current.png")
        elif state == "LOCKED":
            levels_image_path = resource_path("assets\\images\\levels\\locked.png")
        elif state == "COMPLETED":
            levels_image_path = resource_path("assets\\images\\levels\\e-passed.png")
        button = ClickableImage(title_frame, image_path=levels_image_path, image_size=(60, 100), bg=frame.cget('bg'))
        button.grid(row=0, column=i + 2, sticky='w', padx=(10, 0), pady=(20, 0))

    book_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\books\\5.png"), bg=frame.cget('bg'), image_size=(60, 80))
    book_image.grid(row=0, column=user_progress["input"]["total"] + 3, sticky='w', padx=(400, 0), pady=(0, 0))

    back_arrow_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\back_arrow.png"),image_size=(50, 50), callback=lambda: change_screen(Screens.LANDING))
    back_arrow_image.grid(row=0, column=user_progress["input"]["total"] + 3, sticky='w', padx=(470, 0), pady=(20, 0))

    code_frame = tk.Frame(frame, bg=frame.cget('bg'))
    code_frame.grid(row=1, column=0, sticky='w', padx=(40, 0), pady=(10, 0))

    task_output_frame = tk.Frame(frame, bg=frame.cget('bg'))
    task_output_frame.grid(row=1, column=1, sticky='w', padx=(40, 0), pady=(0, 0))

    task_frame = tk.Frame(task_output_frame)
    task_frame.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    task_label = WhiteStormLabel(task_frame,bg=task_frame.cget('bg'),font_size=13, width=60, height=5, text='❧ En el lugar donde se está no hay internet.\nHay que mandar una carta, pero para eso hay que escribir\ntodos los datos del destino. Leer por teclado la dirección\na la que se va a enviar e imprimirla así queda\nen el sobre: “Paroissien 2012”.')
    task_label.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    output_frame = tk.Frame(task_output_frame, bg=frame.cget('bg'))
    output_frame.grid(row=1, column=0, sticky='w', padx=(0, 0), pady=(0, 0))

    input_area = tk.Text(code_frame, width=55, height=25, relief="ridge", borderwidth=3, font=("Courier New", 13))

    if user_completed_stage:
        input_area.insert("1.0",
                          'direccion = input("Ingrese la dirección a donde se enviará la carta: ")\nprint(direccion)')
    else:
        input_area.insert("1.0", '')

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
    music_sheet_image = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-n-4\\4-1.png"),
                                       image_size=(598, 412), bg=output_frame.cget('bg'))
    music_sheet_image.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(20, 0))

def correct_music_sheet(output_frame, code_frame, change_screen, input_area):
    music_sheet_image = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-n-4\\4-2.png"),
                                       image_size=(598, 412), bg=output_frame.cget('bg'))
    music_sheet_image.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(20, 0))
    next_level_button = tk.Button(code_frame, width=7, height=2, text="Next",
                                  command=lambda: change_screen(Screens.INPUT_1))
    next_level_button.grid(row=1, column=0, sticky='e', padx=(0, 0), pady=(10, 10))
    input_area.config(state=tk.DISABLED, cursor="arrow")
