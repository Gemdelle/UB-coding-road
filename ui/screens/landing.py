import tkinter as tk
from PIL import ImageTk, Image

from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.rhombus_button import RombusButton
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path

def draw(frame):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    image = Image.open(resource_path("assets\\images\\book.jpg"))
    resized_image = image.resize((20, 20))
    tk_image = ImageTk.PhotoImage(resized_image)

    row_index = 0
    for key, value in user_progress.items():
        label = WhiteStormLabel(frame, text=f"{row_index}. {key}", font_size=10)
        label.grid(row=row_index+1, column=0, padx=10, pady=10, sticky=tk.W)

        if value["status"] != "LOCKED":
            book_image = tk.Label(frame, image=tk_image)
            book_image.image = tk_image
            book_image.grid(row=row_index+1, column=1, padx=10, pady=10, sticky=tk.W)

        for i in range(value["total"] + 1):
            state = "IN_PROGRESS" if value["status"] == "LOCKED" else "IN_PROGRESS" if value["current"] < i else "COMPLETED"
            button = CircleButton(frame, state=state, width=20, height=20)
            button.grid(row=row_index+1, column=2 + i, padx=10, pady=10, sticky=tk.W)

        test_stats = value["test"]
        rhombus_button = RombusButton(frame, width=20, height=20, text=f"{test_stats['actual']}/{test_stats['total']}")
        rhombus_button.grid(row=row_index+1, column=2 + value["total"] + 1, padx=10, pady=10, sticky=tk.W)

        row_index += 1

        # Place title_label in column 6
    title_label = WhiteStormLabel(frame, text=f"CODING ROAD MAP", font_size=10)
    title_label.grid(row=0, column=6, padx=10, pady=10, sticky=tk.W)

    # Configure column widths before and after title_label
    for i in range(6):  # Columns before title_label
        frame.columnconfigure(i, weight=1)

    frame.columnconfigure(7, weight=1)  # Column after title_label
