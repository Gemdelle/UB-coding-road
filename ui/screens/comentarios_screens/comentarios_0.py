import tkinter as tk
import subprocess

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.clickable_image import ClickableImage
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path


def process_input(input_area, output_label):
    # Get text from text area
    input_text = input_area.get("1.0", "end-1c")

    try:
        # Execute the input as Python code and capture the output
        process = subprocess.Popen(["python", "-c", input_text], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        # Update the label with the output and any system error
        output_label.config(text=f"{stdout.decode()}")
    except Exception as e:
        # If an error occurs during execution, display it in the label
        output_label.config(text="Error: " + str(e))

def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    title_frame = tk.Frame(frame, bg="#3d6466")
    title_frame.grid(row=0, column=0, columnspan=8)

    back_arrow_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\back_arrow.png"), image_size=(60, 60), callback= lambda: change_screen(Screens.LANDING))
    back_arrow_image.grid(row=0, column=0, sticky='w', padx=(20, 0), pady=(20, 0))

    title_label = WhiteStormLabel(title_frame, text=f"0. Comentarios", font_size=20, bg="#3d6466", bd=2, relief="solid", highlightbackground="black")
    title_label.grid(row=0, column=1, sticky='w', padx=(100, 0), pady=(20, 0))

    for i in range(user_progress["comentarios"]["total"]):
        state = "LOCKED" if user_progress["comentarios"]["status"] == "LOCKED" else "IN_PROGRESS" if i == user_progress["comentarios"]["current"] else "LOCKED" if i > user_progress["comentarios"]["current"] else "COMPLETED"
        button = CircleButton(title_frame, status=state, width=20, height=20)
        button.grid(row=0, column=i + 2, sticky='w', padx=(10, 0), pady=(30, 10))

    book_image = ClickableImage(title_frame, image_path=resource_path("assets\\images\\book.jpg"), image_size=(50, 50))
    book_image.grid(row=0, column=user_progress["comentarios"]["total"] + 3, sticky='w', padx=(620, 0), pady=(20, 0))

    code_frame = tk.Frame(frame, bg="#7950f2")
    code_frame.grid(row=1, column=0, sticky='w', padx=(60, 0), pady=(60, 0))

    task_output_frame = tk.Frame(frame, bg="#ffffff")
    task_output_frame.grid(row=1, column=1, sticky='w', padx=(40, 0), pady=(55, 0))

    task_frame = tk.Frame(task_output_frame)
    task_frame.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))
    task_label = WhiteStormLabel(task_frame,anchor="w",font_size=13, width=55, height=8, bg="#0000ff", relief="ridge", borderwidth=3, text='❧ Consigna: Comenta la variable "autor" con el símbolo # para que \n no se tenga en cuenta en la ejecución del programa.')
    task_label.grid(row=0, column=0, sticky='w', padx=(5, 0), pady=(0, 0))

    output_frame = tk.Frame(task_output_frame)
    output_frame.grid(row=1, column=0, sticky='w', padx=(0, 0), pady=(50, 50))
    music_sheet_image = ClickableImage(output_frame, image_path=resource_path("assets\\images\\music_sheet.png"),image_size=(560, 300))
    music_sheet_image.grid(row=0, column=0, sticky='w', padx=(0, 0), pady=(0, 0))
    output_label = tk.Label(output_frame, width=30, height=2, relief="ridge", borderwidth=3, text="", anchor='center', justify='center', wraplength=200)
    output_label.place(in_=music_sheet_image, relx=0.5, rely=0.05, anchor='center')

    input_area = tk.Text(code_frame,width=70, height=30,  relief="ridge", borderwidth=3)
    input_area.insert("1.0", 'autor = "Ludwig van Beethoven"\nprint(autor)')
    input_area.grid(row=0, column=0, sticky='w', padx=(20, 20), pady=(20, 0))

    # Create button to process input
    process_button = tk.Button(code_frame, text="Run", command=lambda: process_input(input_area, output_label))
    process_button.grid(row=1, column=0, sticky='e', padx=(20, 20), pady=(10, 10))

    process_input(input_area, output_label)
