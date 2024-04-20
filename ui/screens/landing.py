import tkinter as tk
from tkinter import YES, BOTH

from PIL import Image, ImageTk

from core.screens import Screens
from core.user_progress_repository import UserProgressRepository
from utils.resource_path_util import resource_path
from utils.sound_manager import SoundManager, play_background_music, play_button_sound

levels=["a","b","c","d","e","f","g","h","i","j","k", "l"]

def draw(frame, change_screen):
    global levels
    repository = UserProgressRepository()
    user_progress = repository.get_current_progress()

    play_background_music()

    canvas = tk.Canvas(frame, bg="black", width=1280, height=720)
    canvas.pack(fill=BOTH, expand=YES)

    image = Image.open(resource_path("assets\\images\\background.jpg"))
    image = image.resize((1280, 720))
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=tk.NW, image=canvas.image)

    canvas.create_text(630, 50, text="Coding Road Map", fill="#e8e8e3", font=("Georgia", 35, "bold"))

    row_index = 0
    row_offset = 50
    for key, value in user_progress.items():
        column_offset = 50
        canvas.create_text(150, 100 + row_offset, text=f"{row_index}. {key.capitalize()}", fill="#e8e8e3", font=("Georgia", 20, "bold"), anchor="nw")

        if value["status"] != "LOCKED":
            image_book = Image.open(resource_path("assets\\images\\books\\"+str(row_index+1)+".png"))
            image_book = image_book.resize((40, 50))
            image_book_tk = ImageTk.PhotoImage(image_book)
            setattr(canvas, f"image_book_{row_index}", image_book_tk)
            canvas.create_image(400, 90 + row_offset, anchor=tk.NW, image=image_book_tk)

        for i in range(value["total"]):
            state = "LOCKED" if value["status"] == "LOCKED" else "IN_PROGRESS" if i == value["current"] else "LOCKED" if i > value["current"] else "COMPLETED"
            screen_to_change = Screens[f'{key}_{i}'.upper()]
            levels_image_path = None
            if state == "IN_PROGRESS":
                levels_image_path = resource_path("assets\\images\\levels\\"+levels[row_index]+"-current.png")
            elif state == "LOCKED":
                levels_image_path = resource_path("assets\\images\\levels\\locked.png")
            elif state == "COMPLETED":
                levels_image_path = resource_path("assets\\images\\levels\\"+levels[row_index]+"-passed.png")

            image_level = Image.open(levels_image_path)
            image_level = image_level.resize((60, 100))
            image_level_tk = ImageTk.PhotoImage(image_level)

            def on_image_click(event, screen=screen_to_change):
                change_screen(screen)
                canvas.destroy()

            def on_image_enter(event):
                canvas.config(cursor="hand2")

            def on_image_leave(event):
                canvas.config(cursor="")

            setattr(canvas, f"image_level_tk_{row_index}_{i}", image_level_tk)
            button = canvas.create_image(430 + column_offset, 80 + row_offset, anchor=tk.NW, image=image_level_tk)
            if state != "LOCKED":
                canvas.tag_bind(button, "<Enter>", on_image_enter)
                canvas.tag_bind(button, "<Leave>", on_image_leave)
                canvas.tag_bind(button, '<Button-1>', on_image_click)

            column_offset += 80

        row_offset += 100
        row_index += 1
