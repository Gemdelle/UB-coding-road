import tkinter as tk
from PIL import ImageTk, Image

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from ui.components.circle_button import CircleButton
from ui.components.rhombus_button import RombusButton
from ui.components.white_storm_label import WhiteStormLabel
from utils.resource_path_util import resource_path


def draw(frame, change_screen):
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    image = Image.open(resource_path("assets\\images\\book.jpg"))
    resized_image = image.resize((20, 20))
    tk_image = ImageTk.PhotoImage(resized_image)

    title_frame = tk.Frame(frame, bg=frame.cget('bg'))
    title_frame.grid(row=0, column=0, columnspan=8)

    title_label = WhiteStormLabel(title_frame, text=f"CODING ROAD MAP", font_size=10, bg="#3d6466")
    title_label.pack(side='right',padx=(500, 0),pady=(10,10))

    body_frame = tk.Frame(frame, bg=frame.cget('bg'))
    body_frame.grid(row=1, column=0, columnspan=8)

    row_index = 0
    for key, value in user_progress.items():
        label = WhiteStormLabel(body_frame, text=f"{row_index}. {key}", font_size=10, bg=frame.cget('bg'))
        label.grid(row=row_index, column=0, padx=10, pady=10, sticky=tk.W)

        if value["status"] != "LOCKED":
            book_image = tk.Label(body_frame, image=tk_image)
            book_image.image = tk_image
            book_image.grid(row=row_index, column=1, padx=10, pady=10, sticky=tk.W)

        for i in range(value["total"]):
            state = "LOCKED" if value["status"] == "LOCKED" else "IN_PROGRESS" if i == value["current"] else "LOCKED" if i > value["current"] else "COMPLETED"
            screen_to_change = Screens[f'{key}_{i}'.upper()]
            button = CircleButton(body_frame, status=state, width=20, height=20, screen_to_change=screen_to_change,bg=frame.cget('bg'), on_click=change_screen, highlightthickness=0)
            button.grid(row=row_index, column=2 + i, padx=10, pady=10, sticky=tk.W)

        test_stats = value["test"]
        rhombus_button = RombusButton(body_frame, width=20, height=20, text=f"{test_stats['actual']}/{test_stats['total']}")
        rhombus_button.grid(row=row_index, column=2 + value["total"] + 1, padx=10, pady=10, sticky=tk.W)

        row_index += 1