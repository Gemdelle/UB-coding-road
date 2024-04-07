import tkinter as tk
import subprocess

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.clickable_image import ClickableImage
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def process_input(input_area, process_button, correct, incorrect, change_screen):
    global comentarios_0_completed
    input_text = input_area.get("1.0", "end-1c")

    try:
        # Execute the input as Python code and capture the output
        process = subprocess.Popen(["python", "-c", input_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Update the label with the output and any system error
        output=stdout.decode()
        if output == "":
            process_button.grid_remove()
            repository = UserProgressRepository()
            correct()
            repository.progress_comentarios()
            change_screen(Screens.LANDING)
        else:
            incorrect()
    except Exception as e:
        # If an error occurs during execution, display it in the label
        #"Error: " + str(e)
        incorrect()

def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    user_completed_stage = user_progress["comentarios"]["current"] > 0

    title_frame = tk.Frame(frame, bg=frame.cget('bg'))
    title_frame.grid(row=0, column=0, columnspan=8)

    back_arrow_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\back_arrow.png"), image_size=(60, 60), callback= lambda: change_screen(Screens.LANDING))
    back_arrow_image.grid(row=0, column=0, sticky='w', padx=(20, 0), pady=(20, 0))

    title_label = WhiteStormLabel(title_frame, text=f"0. Comentarios", font_size=20, bd=2, relief="solid", highlightbackground="black", bg=frame.cget('bg'))
    title_label.grid(row=0, column=1, sticky='w', padx=(100, 0), pady=(20, 0))

    for i in range(user_progress["comentarios"]["total"]):
        state = "LOCKED" if user_progress["comentarios"]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress["comentarios"]["current"] else "LOCKED" if i > user_progress["comentarios"]["current"] else "COMPLETED"
        button = CircleButton(title_frame, status=state, width=20, height=20, bg=title_frame.cget('bg'), highlightthickness=0)
        button.grid(row=0, column=i + 2, sticky='w', padx=(10, 0), pady=(30, 10))

    book_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\book.jpg"), image_size=(50, 50))
    book_image.grid(row=0, column=user_progress["comentarios"]["total"] + 3, sticky='w', padx=(620, 0), pady=(20, 0))

    code_frame = tk.Frame(frame, bg=frame.cget('bg'))
    code_frame.grid(row=1, column=0, sticky='w', padx=(60, 0), pady=(60, 0))

    task_output_frame = tk.Frame(frame, bg=frame.cget('bg'))
    task_output_frame.grid(row=1, column=1, sticky='w', padx=(40, 0), pady=(55, 0))

    task_frame = tk.Frame(task_output_frame, bg=frame.cget('bg'))
    task_frame.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))
    task_label = WhiteStormLabel(task_frame,anchor="w",font_size=13, width=55, height=8, relief="ridge", borderwidth=3, text='❧ Consigna: Comenta la variable "autor" con el símbolo # para que \n no se tenga en cuenta en la ejecución del programa.')
    task_label.grid(row=0, column=0, sticky='w', padx=(5, 0), pady=(0, 0))

    output_frame = tk.Frame(task_output_frame, bg=frame.cget('bg'))
    output_frame.grid(row=1, column=0, sticky='w', padx=(0, 0), pady=(20, 10))
    if user_completed_stage:
        correct_music_sheet(output_frame)
    else:
        incorrect_music_sheet(output_frame)

    input_area = tk.Text(code_frame,width=70, height=30,  relief="ridge", borderwidth=3)
    if user_completed_stage:
        input_area.insert("1.0", '#autor = "Ludwig van Beethoven"\n#print(autor)')
    else:
        input_area.insert("1.0", 'autor = "Ludwig van Beethoven"\nprint(autor)')
    input_area.grid(row=0, column=0, sticky='w', padx=(20, 20), pady=(20, 0))

    if not user_completed_stage:
        # Create button to process input
        process_button = tk.Button(code_frame, text="Run", command=lambda: process_input(input_area, process_button,
                                                                                         lambda: correct_music_sheet(
                                                                                             output_frame),
                                                                                         lambda: incorrect_music_sheet(
                                                                                             output_frame),
                                                                                         change_screen))
        process_button.grid(row=1, column=0, sticky='e', padx=(20, 20), pady=(10, 10))
        process_input(input_area,process_button,lambda: correct_music_sheet(output_frame), lambda: incorrect_music_sheet(output_frame), change_screen)

def incorrect_music_sheet(output_frame):
    music_sheet_image = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-1\\1b.png"),
                                       image_size=(225, 365), bg=output_frame.cget('bg'))
    music_sheet_image.grid(row=0, column=0, sticky='nsew', padx=(210, 0), pady=(0, 0))

def correct_music_sheet(output_frame):
    music_sheet_image = ClickableImage(output_frame, image_path=resource_path("assets\\images\\ex-1\\1a.png"),
                                       image_size=(225, 365), bg=output_frame.cget('bg'))
    music_sheet_image.grid(row=0, column=0, sticky='nsew', padx=(210, 0), pady=(0, 0))
