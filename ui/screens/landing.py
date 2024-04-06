import tkinter as tk
from PIL import ImageTk, Image

from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def draw(frame):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    image = Image.open(resource_path("assets\\images\\book.jpg"))
    resized_image = image.resize((50, 50))
    tk_image = ImageTk.PhotoImage(resized_image)

    row_index = 0
    for key, value in user_progress.items():
        label = WhiteStormLabel(frame, text=f"{row_index}. {key}")
        label.grid(row=row_index, column=0, padx=10, pady=10, sticky=tk.W)

        book_image = tk.Label(frame, image=tk_image)
        book_image.grid(row=row_index, column=1, padx=10, pady=10, sticky=tk.W)

        for i in range(value["total"] + 1):
            state = "IN_PROGRESS" if value["status"] == "LOCKED" else "IN_PROGRESS" if value["current"] < i else "COMPLETED"
            button = CircleButton(frame, state=state, width=40, height=40)
            button.grid(row=row_index, column=2 + i, padx=10, pady=10, sticky=tk.W)

        row_index += 1


